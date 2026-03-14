#!/usr/bin/env python3
"""Render fixture-driven deck previews from cockpitdecks config YAML."""

from __future__ import annotations

import argparse
import math
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from PIL import Image, ImageColor, ImageDraw, ImageFont


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
    screen_size: tuple[int, int]


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

    def render_template(self, template: Any, text_format: str | None = None, context: dict[str, Any] | None = None) -> str:
        if template is None:
            return ""
        context = context or {}
        raw = str(template)

        def replace(match: re.Match[str]) -> str:
            key = match.group(1)
            value = context.get(key)
            if value is None:
                value = self.get_value(key)
            return self._format_value(value, text_format)

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
        image.save(output_path)

    def _load_layout(self) -> Layout:
        decktype = self._load_yaml(self.decktype_path)
        key_button = next(button for button in decktype["buttons"] if button["name"] == 0 and button.get("feedback") == "image")
        screen_button = next(button for button in decktype["buttons"] if button["name"] == "left")
        return Layout(key_size=tuple(key_button["dimension"]), screen_size=tuple(screen_button["dimension"]))

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
        screen_w, screen_h = self.layout.screen_size
        grid_gap = 14
        outer_gap = 18
        grid_w = key_w * 4 + grid_gap * 3
        grid_h = key_h * 3 + grid_gap * 2
        main_x = screen_w + outer_gap
        main_y = 0
        left_x = 0
        right_x = main_x + grid_w + outer_gap
        canvas_w = right_x + screen_w
        canvas_h = max(grid_h, screen_h)

        image = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))

        groups = self._group_buttons(page["buttons"])
        left_screen = self._render_side_screen(groups.get("left"), page)
        right_screen = self._render_side_screen(groups.get("right"), page)
        image.alpha_composite(left_screen, (left_x, max(0, (canvas_h - screen_h) // 2)))
        image.alpha_composite(right_screen, (right_x, max(0, (canvas_h - screen_h) // 2)))

        for index in range(12):
            row, col = divmod(index, 4)
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
        bg = self._color(button.get("text-bg-color", button.get("text_bg_color", "Black")))
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

        label = button.get("label")
        if label:
            label_box = (8, 8, width - 8, 24)
            label_color = self._color(button.get("label-color", self.layout_defaults.get("default-label-color", "white")))
            if annunciator and self._is_dark_color(label_color):
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
            if 0 <= index < len(multi_texts):
                return multi_texts[index].get("text", "")
            return multi_texts[0].get("text", "")
        return button.get("text", "")

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
        return self.evaluator.render_template(part.get("text", ""), part.get("text-format"), context)

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
