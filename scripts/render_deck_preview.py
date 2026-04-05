#!/usr/bin/env python3
"""Render fixture-driven deck previews from cockpitdecks config YAML."""

from __future__ import annotations

import argparse
import base64
import io
import json
import math
import warnings
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from PIL import Image, ImageChops, ImageColor, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
FONT_DIRS = [
    ROOT / "resources" / "fonts",
    ROOT.parent / "cockpitdecks" / "cockpitdecks" / "resources" / "fonts",
    ROOT.parent / "archive" / "cockpitdecks.old" / "cockpitdecks" / "resources" / "fonts",
]
COCKPITDECKS_RESOURCES_CONFIG = ROOT.parent / "cockpitdecks" / "cockpitdecks" / "resources" / "config.yaml"
DEFAULT_COCKPIT_COLOR = "cornflowerblue"

TOKEN_RE = re.compile(r"\$\{[^}]+\}|[^\s]+")
PLACEHOLDER_RE = re.compile(r"\$\{([^}]+)\}")

DEFAULT_DATA = {
    "sim/cockpit2/gauges/indicators/airspeed_kts_pilot": 124,
    "sim/cockpit2/gauges/indicators/compass_heading_deg_mag": 273,
    "sim/cockpit2/gauges/indicators/altitude_ft_pilot": 6500,
    "sim/cockpit2/gauges/actuators/barometer_setting_in_hg_pilot": 29.92,
    "sim/cockpit2/gauges/indicators/vvi_fpm_pilot": 700,
    "sim/cockpit2/fuel/fuel_quantity[0]": 92,
    "sim/cockpit2/fuel/fuel_quantity[1]": 84,
    "sim/cockpit2/engine/indicators/engine_speed_rpm[0]": 2450,
    "sim/cockpit2/engine/indicators/MPR_in_hg[0]": 27.4,
    "sim/cockpit2/engine/indicators/EGT_deg_cel[0]": 1420,
    "sim/cockpit2/engine/indicators/CHT_deg_C[0]": 188,
    "sim/cockpit2/engine/indicators/fuel_flow_kg_sec[0]": 0.00072,
    "sim/flightmodel/engine/ENGN_FF_[0]": 0.00072,
    "sim/cockpit2/engine/indicators/oil_temperature_deg_C[0]": 98,
    "sim/cockpit2/engine/indicators/oil_pressure_psi[0]": 58,
    "sim/cockpit2/transmissions/indicators/oil_temperature": 98,
    "sim/cockpit2/transmissions/indicators/oil_pressure": 58,
    "sim/cockpit/misc/vacuum": 5.1,
    "sim/cockpit/electrical/battery_charge_watt_hr[0]": 24.8,
    "sim/cockpit2/electrical/battery_amps[0]": -3.4,
    "sim/cockpit2/engine/indicators/prop_speed_rpm[0]": 2500,
    "sim/cockpit2/clock_timer/hobbs_time_hours": 321,
    "sim/cockpit2/clock_timer/hobbs_time_minutes": 14,
    "sim/cockpit2/clock_timer/hobbs_time_seconds": 5,
    "sim/cockpit/warnings/annunciators/oil_pressure": 0,
    "sim/cockpit/warnings/annunciators/generator": 0,
    "sim/cockpit/warnings/annunciators/fuel_pressure": 0,
    "sim/cockpit/warnings/annunciators/low_vacuum": 0,
    "sim/cockpit2/radios/indicators/gps_nav_id": "KTRK",
    "sim/cockpit2/radios/indicators/gps_dme_distance_nm": 18.4,
    "sim/cockpit2/radios/indicators/gps_bearing_deg_mag": 276,
    "sim/cockpit2/radios/indicators/gps_dme_time_min": 9,
    "sim/flightmodel/engine/ENGN_thro[0]": 0.74,
    "sim/cockpit/autopilot/heading_mag": 273,
    "sim/cockpit2/autopilot/altitude_dial_ft": 6500,
    "sim/cockpit/autopilot/vertical_velocity": 700,
    "sim/flightmodel/engine/ENGN_mixt[0]": 0.88,
    "sim/cockpit2/autopilot/servos_on": 1,
    "sim/cockpit2/autopilot/flight_director_mode": 1,
    "sim/cockpit2/autopilot/heading_status": 1,
    "sim/cockpit2/autopilot/altitude_hold_status": 1,
    "sim/cockpit2/autopilot/gpss_status": 2,
    "sim/cockpit2/autopilot/vnav_armed": 0,
    "sim/cockpit2/autopilot/approach_status": 0,
    "sim/cockpit2/autopilot/backcourse_status": 0,
    "sim/cockpit2/autopilot/altitude_mode": 4,
    "sim/cockpit/switches/HSI_selector": 2,
    "sim/cockpit2/radios/actuators/transponder_mode": 4,
    "sim/cockpit/radios/transponder_code": 1200,
    "sim/cockpit/radios/transponder_id": 0,
    "sim/cockpit/radios/transponder_light": 1,
    "sim/cockpit/electrical/avionics_on": 1,
    "sim/cockpit2/electrical/battery_on[0]": 1,
    "sim/cockpit2/electrical/battery_on[1]": 1,
    "sim/cockpit2/electrical/generator_on[0]": 1,
    "sim/cockpit2/electrical/generator_on[1]": 1,
    "laminar/sr22/fuel_selector_pos": 1,
}


@dataclass
class Layout:
    key_size: tuple[int, int]
    grid_repeat: tuple[int, int]
    screen_size: tuple[int, int] | None
    has_encoders: bool = False


class FormulaEvaluator:
    def __init__(self, datarefs: dict[str, Any]):
        self.datarefs = {**DEFAULT_DATA, **(datarefs or {})}

    def get_value(self, ref: str) -> Any:
        return self.datarefs.get(ref, 0)

    def eval(self, expr: Any, context: dict[str, Any] | None = None) -> Any:
        if expr is None:
            return None
        if isinstance(expr, (int, float)):
            return expr
        text = str(expr).strip()
        if not text:
            return ""
        context = context or {}
        tokens = TOKEN_RE.findall(text)
        if len(tokens) == 1:
            return self._resolve_token(tokens[0], context)
        stack: list[Any] = []
        for token in tokens:
            if token in {"+", "-", "*", "/", "%", "eq", "min", "max", "roundn"}:
                if token == "roundn":
                    digits = int(self._as_number(stack.pop()))
                    value = self._as_number(stack.pop())
                    stack.append(round(value, digits))
                    continue
                b = self._as_number(stack.pop())
                a = self._as_number(stack.pop())
                if token == "+":
                    stack.append(a + b)
                elif token == "-":
                    stack.append(a - b)
                elif token == "*":
                    stack.append(a * b)
                elif token == "/":
                    stack.append(0 if b == 0 else a / b)
                elif token == "%":
                    stack.append(0 if b == 0 else a % b)
                elif token == "eq":
                    stack.append(1 if a == b else 0)
                elif token == "min":
                    stack.append(min(a, b))
                elif token == "max":
                    stack.append(max(a, b))
            elif token in {"floor", "ceil", "abs", "round"}:
                value = self._as_number(stack.pop())
                if token == "floor":
                    stack.append(math.floor(value))
                elif token == "ceil":
                    stack.append(math.ceil(value))
                elif token == "round":
                    stack.append(round(value))
                else:
                    stack.append(abs(value))
            else:
                stack.append(self._resolve_token(token, context))
        return stack[-1] if stack else None

    @staticmethod
    def _yaml_bool_str(value: Any) -> Any:
        """PyYAML 1.1 parses ON/OFF/YES/NO/TRUE/FALSE as Python booleans.
        Convert them back to their canonical uppercase string form so they
        render correctly on buttons."""
        if value is True:
            return "ON"
        if value is False:
            return "OFF"
        return value

    def render_template(self, template: Any, text_format: str | None = None, context: dict[str, Any] | None = None) -> str:
        if template is None:
            return ""
        context = context or {}
        template = self._yaml_bool_str(template)
        raw = str(template)

        def replace(match: re.Match[str]) -> str:
            key = match.group(1)
            value = context.get(key)
            if value is None:
                value = self.get_value(key)
            # text-format can be a dict mapping dataref names to individual format strings
            fmt = text_format
            if isinstance(text_format, dict):
                fmt = text_format.get(key)
            return self._format_value(value, fmt)

        return PLACEHOLDER_RE.sub(replace, raw)

    @staticmethod
    def _as_number(value: Any) -> float:
        if isinstance(value, bool):
            return 1.0 if value else 0.0
        if isinstance(value, (int, float)):
            return float(value)
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    def _resolve_token(self, token: str, context: dict[str, Any]) -> Any:
        if token.startswith("${") and token.endswith("}"):
            key = token[2:-1]
            return context.get(key, self.get_value(key))
        if token in context:
            return context[token]
        try:
            return float(token)
        except ValueError:
            return token

    @staticmethod
    def _format_value(value: Any, text_format: str | None) -> str:
        if value is None:
            return ""
        if text_format:
            try:
                if "{0" in text_format:
                    return text_format.format(value)
                return text_format.format(value)
            except (IndexError, KeyError, ValueError):
                pass
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value)


class PreviewRenderer:
    def __init__(self, layout_dir: Path, decktype_path: Path, fixture_path: Path | None):
        self.layout_dir = layout_dir
        self.decktype_path = decktype_path
        self.fixture = self._load_yaml(fixture_path) if fixture_path else {}
        self.evaluator = FormulaEvaluator(self.fixture.get("datarefs", {}))
        self.layout_defaults = self._load_yaml(layout_dir / "config.yaml")
        self.deck_defaults = self._load_yaml(layout_dir.parent / "config.yaml")
        self.resources_defaults = self._load_yaml(COCKPITDECKS_RESOURCES_CONFIG)
        self.layout = self._load_layout()

    def render_page(self, page_name: str, output_path: Path) -> None:
        page = self._load_page(page_name)
        image = self._render_composite(page)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if self._png_pixels_match(output_path, image):
            return
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        content = buffer.getvalue()
        if output_path.exists() and output_path.read_bytes() == content:
            return
        output_path.write_bytes(content)

    def _png_pixels_match(self, output_path: Path, image: Image.Image) -> bool:
        if not output_path.exists():
            return False
        with Image.open(output_path) as existing:
            candidate = image.convert("RGBA")
            existing_rgba = existing.convert("RGBA")
            if existing_rgba.size != candidate.size:
                return False
            return ImageChops.difference(existing_rgba, candidate).getbbox() is None

    def _load_layout(self) -> Layout:
        decktype = self._load_yaml(self.decktype_path)
        key_button = next(button for button in decktype["buttons"] if button["name"] == 0 and button.get("feedback") == "image")
        repeat = tuple(key_button.get("repeat", (1, 1)))
        screen_button = next((button for button in decktype["buttons"] if button["name"] == "left" and button.get("feedback") == "image"), None)
        screen_size = tuple(screen_button["dimension"]) if screen_button else None
        has_encoders = any(b.get("prefix") == "e" for b in decktype["buttons"])
        return Layout(key_size=tuple(key_button["dimension"]), grid_repeat=repeat, screen_size=screen_size, has_encoders=has_encoders)

    def _load_page(self, page_name: str) -> dict[str, Any]:
        page_path = self.layout_dir / f"{page_name}.yaml"
        page = self._load_yaml(page_path)
        buttons: list[dict[str, Any]] = []
        includes = [part.strip() for part in str(page.get("includes", "")).split(",") if part.strip()]
        for include in includes:
            include_path = self.layout_dir / f"{include}.yaml"
            include_yaml = self._load_yaml(include_path)
            buttons.extend(include_yaml.get("buttons", []))
        buttons.extend(page.get("buttons", []))
        page["buttons"] = buttons
        return page

    def _render_composite(self, page: dict[str, Any]) -> Image.Image:
        key_w, key_h = self.layout.key_size
        cols, rows = self.layout.grid_repeat
        grid_gap = 8
        outer_gap = 14
        grid_w = key_w * cols + grid_gap * max(cols - 1, 0)
        grid_h = key_h * rows + grid_gap * max(rows - 1, 0)
        screen_w = screen_h = 0
        if self.layout.screen_size:
            screen_w, screen_h = self.layout.screen_size
        main_x = screen_w + outer_gap if self.layout.screen_size else 0
        main_y = 0
        left_x = 0
        right_x = main_x + grid_w + outer_gap if self.layout.screen_size else grid_w
        canvas_w = right_x + screen_w if self.layout.screen_size else grid_w
        canvas_h = max(grid_h, screen_h) if self.layout.screen_size else grid_h

        page_bg = self._page_background_color(page)
        image = Image.new("RGBA", (canvas_w, canvas_h), (*page_bg, 255))

        groups = self._group_buttons(page["buttons"])
        if self.layout.screen_size:
            left_screen = self._render_side_screen(groups.get("left"), page)
            right_screen = self._render_side_screen(groups.get("right"), page)
            image.alpha_composite(left_screen, (left_x, max(0, (canvas_h - screen_h) // 2)))
            image.alpha_composite(right_screen, (right_x, max(0, (canvas_h - screen_h) // 2)))

        for index in range(cols * rows):
            row, col = divmod(index, cols)
            x = main_x + col * (key_w + grid_gap)
            y = main_y + row * (key_h + grid_gap)
            button = groups["grid"].get(index)
            tile = self._render_button(button, page) if button else self._render_empty_button(page)
            image.alpha_composite(tile, (x, y))
        return image

    def _render_button(self, button: dict[str, Any], page: dict[str, Any]) -> Image.Image:
        width, height = self.layout.key_size
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        bg_value = button.get("text-bg-color", button.get("text_bg_color"))
        bg = self._color(bg_value) if bg_value is not None else self._page_background_color(page)
        draw.rectangle((0, 0, width - 1, height - 1), fill=bg, outline=(118, 123, 128), width=2)
        inner = (6, 6, width - 7, height - 7)
        draw.rectangle(inner, outline=(48, 52, 56))

        annunciator = button.get("annunciator")
        if annunciator:
            self._render_annunciator(image, annunciator, button, page)
        else:
            context = self._formula_context(button)
            text_value = self._button_text_value(button, context)
            rendered = self.evaluator.render_template(text_value, button.get("text-format"), context)
            font = self._fit_font(
                button.get("text-font"),
                int(button.get("text-size", self.layout_defaults.get("default-text-size", 24))),
                rendered,
                (width - 16, height - 28),
            )
            self._draw_text_box(draw, (8, 20, width - 8, height - 8), rendered, font, self._color(button.get("text-color", "white")), anchor="mm")

        label = self.evaluator._yaml_bool_str(button.get("label"))
        if label:
            label_box = (8, 8, width - 8, 24)
            label_color = self._color(button.get("label-color", self.layout_defaults.get("default-label-color", "white")))
            if not self._is_dark_color(bg) and self._is_dark_color(label_color):
                draw.rectangle(label_box, fill=(178, 182, 186))
            self._draw_text_box(
                draw,
                label_box,
                str(label),
                self._font(button.get("label-font", self.layout_defaults.get("default-label-font")), int(button.get("label-size", self.layout_defaults.get("default-label-size", 13)))),
                label_color,
                anchor="ma",
            )

        if button.get("type") == "page" and button.get("page") == page.get("name"):
            draw.rectangle((2, 2, width - 3, height - 3), outline=(255, 188, 64), width=3)
        return image

    def _render_empty_button(self, page: dict[str, Any]) -> Image.Image:
        width, height = self.layout.key_size
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        fill = self._page_background_color(page)
        draw.rectangle((0, 0, width - 1, height - 1), fill=fill, outline=(90, 95, 100), width=2)
        draw.rectangle((6, 6, width - 7, height - 7), outline=(36, 40, 44))
        return image

    def _page_background_color(self, page: dict[str, Any]) -> tuple[int, int, int]:
        for key in ("cockpit-color", "default-cockpit-color"):
            for source in (page, self.layout_defaults, self.deck_defaults, self.resources_defaults):
                value = source.get(key)
                if value is not None:
                    return self._color(value)
        return self._color(DEFAULT_COCKPIT_COLOR)

    def _button_text_value(self, button: dict[str, Any], context: dict[str, Any]) -> Any:
        multi_texts = button.get("multi-texts")
        if multi_texts:
            index = int(self.evaluator._as_number(context.get("formula", 0)))
            entry = multi_texts[index] if 0 <= index < len(multi_texts) else multi_texts[0]
            return self.evaluator._yaml_bool_str(entry.get("text", ""))
        return self.evaluator._yaml_bool_str(button.get("text", ""))

    def _render_side_screen(self, button: dict[str, Any] | None, page: dict[str, Any]) -> Image.Image:
        width, height = self.layout.screen_size
        fill = self._page_background_color(page)
        image = Image.new("RGBA", (width, height), (*fill, 255))
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, width - 1, height - 1), fill=fill, outline=(110, 116, 121), width=2)
        if not button or "side" not in button:
            return image
        labels = button["side"].get("labels", [])
        centers = button["side"].get("centers", [16, 50, 84])
        for idx, label in enumerate(labels):
            center = centers[idx] if idx < len(centers) else 16 + idx * 34
            y = round(height * (center / 100.0)) if isinstance(center, (int, float)) and center <= 100 else int(center)
            title_font = self._font(label.get("label-font"), int(label.get("label-size", 14)))
            value_font = self._font(label.get("text-font"), int(label.get("text-size", 18)))
            title = str(label.get("label", ""))
            context = self._formula_context(label)
            rendered = self.evaluator.render_template(label.get("text", ""), label.get("text-format"), context)
            draw.text((width // 2, y - 16), title, font=title_font, fill=self._color(label.get("label-color", "gold")), anchor="ma")
            draw.text((width // 2, y + 8), rendered, font=value_font, fill=self._color(label.get("text-color", "white")), anchor="ma")
        return image

    def _render_annunciator(self, image: Image.Image, annunciator: dict[str, Any], button: dict[str, Any], page: dict[str, Any]) -> None:
        draw = ImageDraw.Draw(image)
        model = annunciator.get("model", "A")
        part_rects = self._annunciator_rects(model, image.size)
        parts = self._annunciator_parts(annunciator)
        off_intensity = self._annunciator_light_off_intensity(button, annunciator, page)
        for part_name, rect in part_rects:
            part = parts.get(part_name)
            if not part:
                continue
            active = bool(self.evaluator.eval(part.get("formula", "1")))
            color = self._color(part.get("color", part.get("text-color", "white")))
            panel_fill = (16, 18, 20)
            draw.rectangle(rect, fill=panel_fill)
            led_style = str(part.get("led", "")).lower()
            if led_style in {"bar", "bars"}:
                led_color = color if active else self._dim(color, off_intensity or 10)
                draw.rectangle((rect[0] + 8, rect[1] + 6, rect[2] - 8, rect[1] + 14), fill=led_color)
            elif led_style == "dot":
                led_color = color if active else self._dim(color, off_intensity or 10)
                cx = (rect[0] + rect[2]) // 2
                cy = (rect[1] + rect[3]) // 2
                r = max(8, min(rect[2] - rect[0], rect[3] - rect[1]) // 5)
                draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=led_color)
            text = self._part_text(part)
            font = self._fit_font(
                part.get("text-font"),
                int(part.get("text-size", 28)),
                text,
                (max(12, rect[2] - rect[0] - 12), max(12, rect[3] - rect[1] - 12)),
            )
            text_color = self._part_text_color(part, active, off_intensity)
            self._draw_text_box(draw, rect, text, font, text_color, anchor="mm")

    def _annunciator_light_off_intensity(self, button: dict[str, Any], annunciator: dict[str, Any], page: dict[str, Any]) -> int | None:
        if "light-off-intensity" in annunciator:
            return annunciator.get("light-off-intensity")
        if "light-off-intensity" in button:
            return button.get("light-off-intensity")
        for source in (page, self.layout_defaults, self.deck_defaults, self.resources_defaults):
            if isinstance(source, dict) and "default-light-off-intensity" in source:
                return source.get("default-light-off-intensity")
        return 10

    def _part_text(self, part: dict[str, Any]) -> str:
        context = self._formula_context(part)
        text = self.evaluator._yaml_bool_str(part.get("text", ""))
        return self.evaluator.render_template(text, part.get("text-format"), context)

    def _part_text_color(self, part: dict[str, Any], active: bool, off_intensity: int | None) -> tuple[int, int, int]:
        if active:
            return self._color(part.get("text-color", part.get("color", "white")))
        if part.get("off-color"):
            return self._color(part["off-color"])
        return self._dim(self._color(part.get("text-color", part.get("color", "white"))), off_intensity or 10)

    @staticmethod
    def _is_dark_color(color: tuple[int, int, int]) -> bool:
        return (color[0] * 299 + color[1] * 587 + color[2] * 114) / 1000 < 72

    @staticmethod
    def _annunciator_parts(annunciator: dict[str, Any]) -> dict[str, Any]:
        parts = annunciator.get("parts")
        if isinstance(parts, dict) and parts:
            return parts
        return {
            key: value
            for key, value in annunciator.items()
            if isinstance(value, dict) and re.fullmatch(r"[A-Z]\d+", str(key))
        }

    @staticmethod
    def _annunciator_rects(model: str, size: tuple[int, int]) -> list[tuple[str, tuple[int, int, int, int]]]:
        width, height = size
        content = (8, 22, width - 8, height - 8)
        x0, y0, x1, y1 = content
        if model == "A":
            return [("A0", content)]
        if model == "B":
            mid = y0 + (y1 - y0) // 2
            return [("B0", (x0, y0, x1, mid - 3)), ("B1", (x0, mid + 3, x1, y1))]
        if model == "D":
            split = y0 + int((y1 - y0) * 0.58)
            mid = x0 + (x1 - x0) // 2
            return [("D0", (x0, y0, x1, split - 3)), ("D1", (x0, split + 3, mid - 3, y1)), ("D2", (mid + 3, split + 3, x1, y1))]
        if model == "F":
            mid_x = x0 + (x1 - x0) // 2
            mid_y = y0 + (y1 - y0) // 2
            return [
                ("F0", (x0, y0, mid_x - 3, mid_y - 3)),
                ("F1", (mid_x + 3, y0, x1, mid_y - 3)),
                ("F2", (x0, mid_y + 3, mid_x - 3, y1)),
                ("F3", (mid_x + 3, mid_y + 3, x1, y1)),
            ]
        return [(next(iter(model), "A0"), content)]

    def _formula_context(self, config: dict[str, Any]) -> dict[str, Any]:
        context: dict[str, Any] = {}
        formula = config.get("formula")
        if formula is not None:
            context["formula"] = self.evaluator.eval(formula)
        return context

    @staticmethod
    def _group_buttons(buttons: list[dict[str, Any]]) -> dict[str, Any]:
        grid: dict[int, dict[str, Any]] = {}
        bar: dict[int, dict[str, Any]] = {}
        side: dict[str, dict[str, Any]] = {}
        for button in buttons:
            index = button.get("index")
            if isinstance(index, int):
                grid[index] = button
            elif isinstance(index, str) and index.startswith("b"):
                bar[int(index[1:])] = button
            elif index in {"left", "right"}:
                side[index] = button
        return {"grid": grid, "bar": bar, **side}

    @staticmethod
    def _load_yaml(path: Path | None) -> dict[str, Any]:
        if path is None or not path.exists():
            return {}
        with path.open("r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle) or {}
        if not isinstance(data, dict):
            raise ValueError(f"{path} must contain a YAML mapping")
        return data

    def _font(self, font_name: str | None, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        if font_name:
            for directory in FONT_DIRS:
                candidate = directory / font_name
                if candidate.exists():
                    try:
                        return ImageFont.truetype(str(candidate), size=size)
                    except OSError:
                        break
        try:
            return ImageFont.truetype("DejaVuSans.ttf", size=size)
        except OSError:
            return ImageFont.load_default()

    def _fit_font(
        self,
        font_name: str | None,
        max_size: int,
        text: str,
        bounds: tuple[int, int],
        min_size: int = 6,
    ) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        max_width, max_height = bounds
        chosen = self._font(font_name, max_size)
        probe = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
        draw = ImageDraw.Draw(probe)
        for size in range(max_size, min_size - 1, -1):
            font = self._font(font_name, size)
            chosen = font
            bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=1, align="center")
            width = bbox[2] - bbox[0]
            height = bbox[3] - bbox[1]
            if width <= max_width and height <= max_height:
                chosen = font
                break
        return chosen

    @staticmethod
    def _color(value: Any) -> tuple[int, int, int]:
        if isinstance(value, (tuple, list)):
            return tuple(int(v) for v in value[:3])
        if value is None:
            return (255, 255, 255)
        text = str(value).strip()
        if text.startswith("(") and text.endswith(")"):
            parts = [int(part.strip()) for part in text[1:-1].split(",")]
            return tuple(parts[:3])
        try:
            return ImageColor.getrgb(text)
        except ValueError:
            return (255, 255, 255)

    @staticmethod
    def _dim(color: tuple[int, int, int], divisor: int) -> tuple[int, int, int]:
        factor = max(divisor, 1)
        return tuple(max(18, int(channel / factor * 2)) for channel in color)

    @staticmethod
    def _draw_text_box(
        draw: ImageDraw.ImageDraw,
        rect: tuple[int, int, int, int],
        text: str,
        font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
        fill: tuple[int, int, int],
        anchor: str,
    ) -> None:
        x0, y0, x1, y1 = rect
        x = (x0 + x1) // 2
        y = (y0 + y1) // 2
        draw.multiline_text((x, y), text, font=font, fill=fill, anchor=anchor, align="center", spacing=1)



class SVGRenderer:
    """Generate self-contained interactive HTML deck previews using PIL-rendered page images.

    Each page is rendered pixel-accurately by PreviewRenderer and embedded as a base64 PNG.
    Transparent SVG overlays on page-type buttons enable JS-powered page switching.
    The hardware chrome (encoder knobs, pager strip, device frame) is drawn in SVG.
    """

    def __init__(
        self,
        layout_dir: Path,
        decktype_path: Path,
        fixture_path: Path | None,
        repo_blob_url_fn: Any = None,
    ):
        self.layout_dir = layout_dir
        self.decktype_path = decktype_path
        self.repo_blob_url_fn = repo_blob_url_fn
        # Delegate all rendering to PreviewRenderer
        self._preview = PreviewRenderer(layout_dir, decktype_path, fixture_path)
        self.layout = self._preview.layout

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _load_yaml(path: Path | None) -> dict[str, Any]:
        if path is None or not path.exists():
            return {}
        with path.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh) or {}
        return data if isinstance(data, dict) else {}

    @staticmethod
    def _xml_escape(text: str) -> str:
        return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    @staticmethod
    def _color_hex(value: Any) -> str:
        if isinstance(value, (tuple, list)):
            r, g, b = (int(v) for v in list(value)[:3])
            return f"#{r:02x}{g:02x}{b:02x}"
        if value is None:
            return "#ffffff"
        text = str(value).strip()
        if text.startswith("(") and text.endswith(")"):
            parts = [int(p.strip()) for p in text[1:-1].split(",")]
            r, g, b = parts[:3]
            return f"#{r:02x}{g:02x}{b:02x}"
        try:
            r, g, b = ImageColor.getrgb(text)[:3]
            return f"#{r:02x}{g:02x}{b:02x}"
        except (ValueError, AttributeError):
            _named = {
                "black": "#000000", "white": "#ffffff", "red": "#ff0000", "lime": "#00ff00",
                "green": "#008000", "blue": "#0000ff", "yellow": "#ffff00", "orange": "#ffa500",
                "gold": "#ffd700", "gray": "#808080", "grey": "#808080", "cyan": "#00ffff",
                "magenta": "#ff00ff", "purple": "#800080", "cornflowerblue": "#6495ed",
                "pink": "#ffc0cb", "silver": "#c0c0c0", "teal": "#008080",
            }
            return _named.get(text.lower(), "#888888")

    @staticmethod
    def _dim_hex(color_hex: str, divisor: int) -> str:
        factor = max(divisor, 1)
        h = color_hex.lstrip("#")
        if len(h) == 3:
            h = h[0] * 2 + h[1] * 2 + h[2] * 2
        if len(h) != 6:
            return "#121212"
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return f"#{max(18, int(r / factor * 2)):02x}{max(18, int(g / factor * 2)):02x}{max(18, int(b / factor * 2)):02x}"

    @staticmethod
    def _group_buttons(buttons: list[dict[str, Any]]) -> dict[str, Any]:
        grid: dict[int, dict[str, Any]] = {}
        enc: dict[int, dict[str, Any]] = {}
        side: dict[str, dict[str, Any]] = {}
        for btn in buttons:
            idx = btn.get("index")
            if isinstance(idx, int):
                grid[idx] = btn
            elif idx in {"left", "right"}:
                side[idx] = btn
            elif isinstance(idx, str) and idx.startswith("e"):
                try:
                    enc[int(idx[1:])] = btn
                except ValueError:
                    pass
        return {"grid": grid, "enc": enc, **side}

    def _page_to_b64_png(self, page_name: str) -> tuple[str, int, int]:
        """Render a page via PIL and return (base64_png_data_uri, width, height)."""
        page = self._preview._load_page(page_name)
        img = self._preview._render_composite(page)
        buf = io.BytesIO()
        img.save(buf, "PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        return f"data:image/png;base64,{b64}", img.width, img.height

    # ------------------------------------------------------------------
    # Hardware chrome SVG helpers
    # ------------------------------------------------------------------

    def _encoder_column_svg(self, encoders: list[Any], x: int, y: int, w: int, h: int) -> str:
        """Render 3 encoder knobs in a vertical column at absolute canvas coordinates."""
        cx = x + w // 2
        enc_r = min(w // 2 - 6, 20)
        thirds = [h // 6, h // 2, h * 5 // 6]
        out: list[str] = []
        for btn, ey in zip(encoders, thirds):
            ey_abs = y + ey
            raw_name = btn.get("name") if btn else None
            name = "" if (raw_name is None or isinstance(raw_name, bool)) else str(raw_name).upper().replace("_", " ")
            out.append(f'<circle cx="{cx}" cy="{ey_abs}" r="{enc_r}" fill="#303030" stroke="#555" stroke-width="1.5"/>')
            out.append(f'<circle cx="{cx}" cy="{ey_abs}" r="{enc_r - 5}" fill="#222" stroke="#444" stroke-width="1"/>')
            out.append(f'<circle cx="{cx}" cy="{ey_abs - enc_r + 4}" r="2.5" fill="#888"/>')
            if name:
                fs = max(7, min(9, w * 9 // (len(name) * 6 + 4)))
                out.append(
                    f'<text x="{cx}" y="{ey_abs + enc_r + 10}" text-anchor="middle" '
                    f'font-size="{fs}" font-family="system-ui,sans-serif" fill="#999">'
                    f'{self._xml_escape(name[:10])}</text>'
                )
        return "".join(out)

    def _pager_strip_svg(self, pager_buttons: dict[int, Any], hw_w: int, y: int, h: int, active_page: str) -> str:
        """Render the Loupedeck Live pager button strip as circular LEDs with slot numbers.

        Slot 0 shows a filled dot (like the physical hardware); slots 1-7 show the slot number.
        The active button glows at full color; others are dimmed.
        """
        n_slots = 8
        slot_w = hw_w // n_slots
        r = max(8, min(h // 2 - 6, 14))   # circle radius
        cy = y + h // 2                    # vertical centre of strip
        out: list[str] = [f'<rect x="0" y="{y}" width="{hw_w}" height="{h}" fill="#111"/>']
        for slot in range(n_slots):
            btn = pager_buttons.get(slot)
            cx = slot * slot_w + slot_w // 2
            target = str(btn.get("page", "")).strip() if btn else ""
            color_name = str(btn.get("colored-led", "")).strip() if btn else ""
            full_color = self._color_hex(color_name) if color_name else "#555555"
            dim_color = self._dim_hex(full_color, 3)
            is_active = target == active_page
            fill = full_color if is_active else dim_color
            active_cls = " active" if is_active else ""
            onclick = f' onclick="showPage(\'{target}\')"' if target else ""
            tooltip = f'<title>→ {self._xml_escape(target)}</title>' if target else ""
            out.append(f'<g id="pb-{target}" class="pb{active_cls}" cursor="pointer"{onclick}>{tooltip}')
            # Outer ring (always visible at dim level; brightens when active)
            out.append(f'<circle class="pb-bg" cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{full_color}" stroke-width="1.5"/>')
            # Active ring overlay (shown via CSS .pb.active .pb-ring)
            out.append(f'<circle class="pb-ring" cx="{cx}" cy="{cy}" r="{r + 3}" fill="none" stroke="#fff" stroke-width="1.5"/>')
            # Label: slot 0 → filled dot; slots 1-7 → number
            if slot == 0:
                dot_r = max(3, r // 3)
                out.append(f'<circle cx="{cx}" cy="{cy}" r="{dot_r}" fill="#fff"/>')
            else:
                out.append(
                    f'<text x="{cx}" y="{cy}" text-anchor="middle" dominant-baseline="middle" '
                    f'font-size="{max(8, r - 2)}" font-family="system-ui,sans-serif" font-weight="bold" fill="#fff">'
                    f'{slot}</text>'
                )
            out.append('</g>')
        return "".join(out)

    # ------------------------------------------------------------------
    # JSON conversion helpers (for deck-render.js canvas renderer)
    # ------------------------------------------------------------------

    @staticmethod
    def _json_safe(value: Any) -> Any:
        """Recursively convert Python types to JSON-serializable values."""
        if isinstance(value, bool):
            return value
        if isinstance(value, dict):
            return {str(k): SVGRenderer._json_safe(v) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return [SVGRenderer._json_safe(v) for v in value]
        if isinstance(value, (int, float)):
            return value
        if value is None:
            return None
        return str(value)

    def _page_to_json(self, page: dict[str, Any]) -> dict[str, Any]:
        """Convert a loaded page dict to a JSON-serializable structure for deck-render.js."""
        groups = self._group_buttons(page.get("buttons", []))
        grid = {str(k): self._json_safe(v) for k, v in groups.get("grid", {}).items()}
        enc  = {str(k): self._json_safe(v) for k, v in groups.get("enc", {}).items()}
        left  = self._json_safe(groups.get("left"))
        right = self._json_safe(groups.get("right"))

        result: dict[str, Any] = {}
        for key in (
            "name", "description", "cockpit-color", "default-cockpit-color",
            "default-text-size", "default-label-size", "default-label-color",
            "default-label-font", "default-light-off-intensity",
        ):
            if key in page:
                result[key] = self._json_safe(page[key])

        result["buttons"] = {"grid": grid, "enc": enc, "left": left, "right": right}
        return result

    def _load_pager_json(self) -> dict[str, Any]:
        """Load pager YAML and return {slot_str: button_data} for deck-render.js."""
        pager_yaml: dict[str, Any] = {}
        for _pc in [self.layout_dir / "pager.yaml", self.layout_dir / "includes" / "pager.yaml"]:
            _data = self._load_yaml(_pc)
            if _data.get("buttons"):
                pager_yaml = _data
                break
        result: dict[str, Any] = {}
        for btn in pager_yaml.get("buttons", []):
            idx = btn.get("index", "")
            if isinstance(idx, str) and idx.startswith("b"):
                try:
                    result[str(int(idx[1:]))] = self._json_safe(btn)
                except ValueError:
                    pass
        return result

    def yaml_to_json(self, page_names: list[str]) -> dict[str, Any]:
        """Convert YAML layout + pages to a DECK_CONFIG dict consumed by deck-render.js."""
        pages_json: dict[str, Any] = {}
        for name in page_names:
            try:
                page = self._preview._load_page(name)
                pages_json[name] = self._page_to_json(page)
            except Exception:
                pass

        lay = self.layout
        layout_json: dict[str, Any] = {
            "keySize":    list(lay.key_size),
            "gridRepeat": list(lay.grid_repeat),
            "screenSize": list(lay.screen_size) if lay.screen_size else None,
            "hasEncoders": lay.has_encoders,
            "gridGap":  8,
            "outerGap": 14,
            "encColW":  54,
            "encGap":    6,
            "padV":     10,
            "pagerH":   42,
        }

        defaults: dict[str, Any] = {}
        for key in (
            "cockpit-color", "default-cockpit-color", "default-text-size",
            "default-label-size", "default-label-color", "default-label-font",
            "default-light-off-intensity",
        ):
            for source in (
                self._preview.layout_defaults,
                self._preview.deck_defaults,
                self._preview.resources_defaults,
            ):
                if key in source:
                    defaults[key] = self._json_safe(source[key])
                    break

        return {
            "layout":   layout_json,
            "defaults": defaults,
            "datarefs": self._json_safe(self._preview.evaluator.datarefs),
            "pager":    self._load_pager_json(),
            "pages":    pages_json,
        }

    @staticmethod
    def _collect_font_names(pages_json: dict[str, Any]) -> set[str]:
        """Collect all text-font and label-font values across all pages."""
        fonts: set[str] = set()

        def _scan(obj: Any) -> None:
            if isinstance(obj, dict):
                for key in ("text-font", "label-font", "text_font", "label_font"):
                    if obj.get(key):
                        fonts.add(str(obj[key]).strip())
                for v in obj.values():
                    _scan(v)
            elif isinstance(obj, list):
                for item in obj:
                    _scan(item)

        _scan(pages_json)
        return fonts

    @staticmethod
    def _collect_codepoints_for_font(pages_json: dict[str, Any], font_name: str) -> set[int]:
        """Collect unicode codepoints used in text fields that reference font_name."""
        codepoints: set[int] = set()

        def _scan(obj: Any) -> None:
            if isinstance(obj, dict):
                # Check if this object uses the target font
                for font_key in ("text-font", "text_font"):
                    if str(obj.get(font_key) or "").strip() == font_name:
                        text = obj.get("text") or obj.get("label") or ""
                        for ch in str(text):
                            codepoints.add(ord(ch))
                for label_key in ("label-font", "label_font"):
                    if str(obj.get(label_key) or "").strip() == font_name:
                        label = obj.get("label") or ""
                        for ch in str(label):
                            codepoints.add(ord(ch))
                for v in obj.values():
                    _scan(v)
            elif isinstance(obj, list):
                for item in obj:
                    _scan(item)

        _scan(pages_json)
        return codepoints

    @staticmethod
    def _subset_font(font_path: Path, codepoints: set[int]) -> bytes | None:
        """Use fontTools to subset a font to the given codepoints. Returns bytes or None."""
        try:
            from fontTools import subset as ft_subset
        except ImportError:
            return None
        if not codepoints:
            return None
        buf = io.BytesIO()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                tt = ft_subset.load_font(str(font_path), ft_subset.Options())
                subsetter = ft_subset.Subsetter(options=ft_subset.Options(
                    name_IDs=["*"],
                    name_legacy=True,
                    name_languages=["*"],
                    hinting=False,
                    desubroutinize=True,
                    notdef_outline=True,
                ))
                subsetter.populate(unicodes=codepoints)
                subsetter.subset(tt)
                tt.save(buf)
                return buf.getvalue()
            except Exception:
                return None

    # Map font name/alias → (filename, CSS family)
    _FONT_ALIAS: dict[str, tuple[str, str]] = {
        "DIN Bold":               ("D-DIN-Bold.otf",          "D-DIN-Bold"),
        "D-DIN Bold":             ("D-DIN-Bold.otf",          "D-DIN-Bold"),
        "D-DIN-Bold":             ("D-DIN-Bold.otf",          "D-DIN-Bold"),
        "D-DIN-Bold.otf":         ("D-DIN-Bold.otf",          "D-DIN-Bold"),
        "D-DIN.otf":              ("D-DIN.otf",               "D-DIN"),
        "DIN Condensed Light":    ("D-DINCondensed.otf",      "D-DINCondensed"),
        "DIN Condensed Regular":  ("D-DINCondensed.otf",      "D-DINCondensed"),
        "DIN Condensed Black.otf":("D-DINCondensed-Bold.otf", "D-DINCondensed-Bold"),
        "DIN Condensed Black":    ("D-DINCondensed-Bold.otf", "D-DINCondensed-Bold"),
        "D-DINCondensed.otf":     ("D-DINCondensed.otf",      "D-DINCondensed"),
        "D-DINCondensed-Bold.otf":("D-DINCondensed-Bold.otf", "D-DINCondensed-Bold"),
        "D-DINExp.otf":           ("D-DINExp.otf",            "D-DINExp"),
        "D-DINExp-Bold.otf":      ("D-DINExp-Bold.otf",       "D-DINExp-Bold"),
        "Seven Segment.ttf":      ("Segment7Standard.otf",    "Segment7Standard"),
        "Segment7Standard.otf":   ("Segment7Standard.otf",    "Segment7Standard"),
        "B612Mono-Regular.ttf":   ("B612Mono-Regular.ttf",    "B612 Mono"),
        "B612-Bold":              ("B612Mono-Regular.ttf",    "B612 Mono"),
        "DejaVuSans.ttf":         ("DejaVuSans.ttf",          "DejaVu Sans"),
        "DejaVuSansMono.ttf":     ("DejaVuSansMono.ttf",      "DejaVu Sans Mono"),
        "DIN Medium.ttf":         ("D-DIN.otf",               "D-DIN"),
        "fontawesome.otf":        ("fontawesome.otf",         "FontAwesome"),
        "Font Awesome 6 Free-Regular-400.otf": ("Font Awesome 6 Free-Regular-400.otf", "Font Awesome 6 Free"),
        "Font Awesome 6 Free-Solid-900.otf":   ("Font Awesome 6 Free-Solid-900.otf",   "Font Awesome 6 Free Solid"),
    }

    def _embed_fonts(self, font_names: set[str], pages_json: dict[str, Any] | None = None,
                     max_bytes: int = 150_000) -> str:
        """Return CSS @font-face declarations for the given font names.

        Small fonts (≤ max_bytes) are embedded whole.  Larger fonts are subsetted
        via fontTools to only the codepoints actually used in pages_json, then
        embedded.  Fonts that cannot be found or subsetted are silently skipped.
        """
        seen: set[str] = set()
        decls: list[str] = []

        for name in sorted(font_names):
            info = self._FONT_ALIAS.get(name)
            if not info:
                lower = name.lower()
                for k, v in self._FONT_ALIAS.items():
                    if k.lower() == lower or v[0].lower() == lower:
                        info = v
                        break
            if not info:
                continue
            filename, family = info
            if filename in seen:
                continue
            seen.add(filename)

            font_path: Path | None = None
            for d in FONT_DIRS:
                candidate = d / filename
                if candidate.exists():
                    font_path = candidate
                    break
            if not font_path:
                continue

            font_bytes: bytes | None = None
            file_size = font_path.stat().st_size

            if file_size <= max_bytes:
                # Small enough to embed whole
                font_bytes = font_path.read_bytes()
            elif pages_json is not None:
                # Large font — subset to only the codepoints used with this font name
                codepoints = self._collect_codepoints_for_font(pages_json, name)
                if not codepoints:
                    # Also check canonical filename as key
                    codepoints = self._collect_codepoints_for_font(pages_json, filename)
                if codepoints:
                    font_bytes = self._subset_font(font_path, codepoints)

            if not font_bytes:
                continue

            ext = font_path.suffix.lower().lstrip(".")
            mime = "font/otf" if ext == "otf" else "font/ttf"
            fmt  = "opentype" if ext == "otf" else "truetype"
            b64  = base64.b64encode(font_bytes).decode()
            decls.append(
                f'@font-face{{font-family:"{family}";'
                f'src:url(data:{mime};base64,{b64}) format("{fmt}");}}'
            )

        return "\n".join(decls)

    # ------------------------------------------------------------------
    # Interactive deck HTML  (Canvas 2D via deck-render.js)
    # ------------------------------------------------------------------

    def render_interactive_deck(self, page_names: list[str], home_page: str) -> str:
        """Render a self-contained interactive HTML deck preview.

        Uses the Canvas 2D deck-render.js renderer.  All pages are serialised to
        a DECK_CONFIG JSON object; deck-render.js draws them client-side without
        any server or PIL dependency.  Fonts used in the layout are embedded as
        base64 @font-face declarations (up to 150 KB per font file).
        """
        # Build DECK_CONFIG
        config = self.yaml_to_json(page_names)
        config_json = json.dumps(config, ensure_ascii=False, separators=(",", ":"))

        # Load deck-render.js from the same directory as this script
        render_js_path = Path(__file__).parent / "deck-render.js"
        render_js = (
            render_js_path.read_text(encoding="utf-8")
            if render_js_path.exists()
            else "/* deck-render.js not found */"
        )

        # Collect and embed fonts
        font_names = self._collect_font_names(config["pages"])
        # Always include the most common deck fonts
        font_names.update({"Segment7Standard.otf", "D-DIN-Bold.otf", "D-DINCondensed.otf"})
        font_css = self._embed_fonts(font_names, pages_json=config["pages"])

        # Compute canvas pixel dimensions (mirrors _computeLayout in deck-render.js)
        lay = self.layout
        kw, kh = lay.key_size
        cols, rows = lay.grid_repeat
        gap = 8
        outer = 14
        enc_col_w, enc_gap, pad_v = 54, 6, 10
        pager_h = 42 if lay.has_encoders else 0
        grid_w = kw * cols + gap * max(cols - 1, 0)
        grid_h = kh * rows + gap * max(rows - 1, 0)
        screen_w = screen_h = 0
        if lay.screen_size:
            screen_w, screen_h = lay.screen_size
        lcd_w = (screen_w + outer + grid_w + outer + screen_w) if lay.screen_size else grid_w
        lcd_h = max(grid_h, screen_h) if lay.screen_size else grid_h
        hw_w = (enc_col_w + enc_gap + lcd_w + enc_gap + enc_col_w) if lay.has_encoders else (pad_v + lcd_w + pad_v)
        hw_h = pad_v + lcd_h + pad_v + pager_h

        init_js = (
            "document.fonts.ready.then(function(){"
            "var c=document.getElementById('deck');"
            f"var r=new DeckRenderer(c,DECK_CONFIG);"
            f"r.showPage({json.dumps(home_page)});"
            "});"
        )

        return (
            '<!DOCTYPE html>\n<html lang="en"><head>\n'
            '<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            "<style>\n"
            + font_css
            + "\nhtml,body{margin:0;padding:0;background:transparent;overflow:hidden}\n"
            "canvas{display:block;max-width:100%}\n"
            "</style>\n"
            "</head>\n<body>\n"
            f'<canvas id="deck" width="{hw_w}" height="{hw_h}"></canvas>\n'
            f"<script>\n{render_js}\n</script>\n"
            f"<script>\nconst DECK_CONFIG={config_json};\n{init_js}\n</script>\n"
            "</body></html>"
        )

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--layout-dir", type=Path, required=True, help="Path to the deck layout directory, e.g. decks/cirrus-sr22/deckconfig/loupedecklive1")
    parser.add_argument("--decktype", type=Path, default=ROOT / "decktypes" / "Loupedeck Live.yaml", help="Deck type YAML to use for button dimensions")
    parser.add_argument("--fixture", type=Path, help="Fixture YAML with sample datarefs")
    parser.add_argument("--page", action="append", required=True, help="Page name to render, repeat for multiple pages")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory where rendered PNGs will be written")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    renderer = PreviewRenderer(args.layout_dir, args.decktype, args.fixture)
    for page in args.page:
        renderer.render_page(page, args.output_dir / f"{page}.png")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
