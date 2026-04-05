#!/usr/bin/env python3
"""Regenerate deck overview docs from config."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any
import os
import tempfile

import re
import sys

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    from render_deck_preview import SVGRenderer
    _SVG_RENDERER_AVAILABLE = True
except ImportError:
    _SVG_RENDERER_AVAILABLE = False


ROOT = Path(__file__).resolve().parents[1]
DECKS_DIR = ROOT / "decks"
DOCS_DECKS_DIR = ROOT / "docs" / "decks"
IMAGE_ROOT = ROOT / "docs" / "assets" / "images"
DECKTYPES_DIR = ROOT / "decktypes"
RENDER_PREVIEW_SCRIPT = ROOT / "scripts" / "render_deck_preview.py"
REPO_BLOB_BASE = "https://github.com/dlicudi/cockpitdecks-configs/blob/main"
MKDOCS_CONFIG = ROOT / "mkdocs.yml"

_STRIP_DEVICE_SUFFIX = re.compile(
    r"\s+for\s+(?:Loupedeck(?:\s+Live)?(?:\s+[SC]T?)?|Stream\s*[Dd]eck(?:\s+\w+)?|\d+\s+keys?|Toliss|Laminar\s+Research|X-Plane).*$",
    re.IGNORECASE,
)

REQUIRES_LABELS: dict[str, str] = {
    "cockpitdecks": "Cockpitdecks",
    "xplane": "X-Plane",
    "PI_CockpitdecksFMSBrowser": "FMS Browser Plugin",
    "PI_CockpitdecksFMSLoader": "FMS Loader Plugin",
}

# Fallback display titles for generated docs when a page YAML has no `_docs.title`,
# `description`, or distinct `name`. Prefer per-page `_docs: { title: "..." }` in deck YAML.
PAGE_NAME_OVERRIDES = {
    "audiopanel": "Audio Panel",
    "home": "Home",
    "index": "Home",
    "mfd": "MFD",
    "pfd": "PFD",
    "pfi": "PFI",
    "fcu": "FCU",
    "fcu2": "FCU 2",
    "g1000": "G1000",
    "gcu478": "GCU478",
    "switches": "Switches",
    "switches2": "Switches 2",
    "icing": "Ice Protection",
    "switchesicing": "Ice Protection",
    "switcheslights": "Lights",
}


_SVG_DIM_RE = re.compile(r'<svg[^>]*\bwidth="(\d+)"[^>]*\bheight="(\d+)"')


def _svg_dimensions(path: Path) -> tuple[int, int] | None:
    """Return (width, height) from the first <svg> tag, or None if unparseable."""
    try:
        header = path.read_text(encoding="utf-8", errors="ignore")[:512]
        m = _SVG_DIM_RE.search(header)
        if m:
            return int(m.group(1)), int(m.group(2))
    except OSError:
        pass
    return None


def run(args: list[str]) -> None:
    subprocess.run(args, check=True, cwd=ROOT)


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return data


def load_pack_metadata(slug: str) -> dict[str, Any]:
    path = DECKS_DIR / slug / "manifest.yaml"
    if not path.exists():
        return {}
    return load_yaml(path)


def write_bytes_if_changed(path: Path, content: bytes) -> bool:
    if path.exists() and path.read_bytes() == content:
        return False
    path.write_bytes(content)
    return True


def write_text_if_changed(path: Path, content: str) -> bool:
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def titleize_slug(slug: str) -> str:
    return " ".join(part.upper() if part.isupper() else part.capitalize() for part in slug.replace("-", " ").split())


def humanize_deck_type(value: str) -> str:
    mapping = {
        "LoupedeckLive": "Loupedeck Live",
        "Stream Deck XL": "Stream Deck XL",
        "StreamDeckXL": "Stream Deck XL",
    }
    if value in mapping:
        return mapping[value]
    text = value.replace("-", " ").replace("_", " ").strip()
    if not text:
        return value
    text = text.replace("Deck", " Deck").replace("Live", " Live").replace("XL", " XL")
    return " ".join(text.split())



def rel_path(target: Path, doc_path: Path) -> str:
    return os.path.relpath(target, doc_path.parent).replace("\\", "/")


def repo_blob_url(path: Path) -> str:
    return f"{REPO_BLOB_BASE}/{path.relative_to(ROOT).as_posix()}"



def normalize_docs_metadata(meta: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(meta, dict):
        return {}
    return meta


def _clean_description(desc: str) -> str | None:
    """Clean a page description for use as a display title, or return None to fall through."""
    s = desc.strip()
    if not s or s in {"Switch Panel", "Switches"}:
        return None
    if s.lower().startswith("include with"):
        return None
    s = _STRIP_DEVICE_SUFFIX.sub("", s).strip()
    if re.match(r"^Main\s+\S+\s+page\s*$", s, re.IGNORECASE):
        return None
    return s or None


def resolve_repo_path(value: str | Path | None, base_dir: Path | None = None) -> Path | None:
    if value is None:
        return None
    candidate = Path(str(value))
    if candidate.is_absolute():
        return candidate
    if base_dir is not None:
        base_candidate = base_dir / candidate
        if base_candidate.exists():
            return base_candidate
    return ROOT / candidate


def layout_config(layout_dir: Path) -> dict[str, Any]:
    config_path = layout_dir / "config.yaml"
    if not config_path.exists():
        return {}
    return load_yaml(config_path)


def layout_docs_metadata(layout_dir: Path) -> dict[str, Any]:
    config = layout_config(layout_dir)
    docs_meta = config.get("_docs") or config.get("docs")
    return docs_meta if isinstance(docs_meta, dict) else {}


def home_page_name(layout_dir: Path) -> str | None:
    config = layout_config(layout_dir)
    candidates = (
        config.get("home-page"),
        config.get("default-homepage-name"),
        config.get("home-page-name"),
    )
    for candidate in candidates:
        text = str(candidate or "").strip()
        if text:
            return text
    return "index"


def docs_entry_page_name(layout_dir: Path, page_map: dict[str, Path]) -> str | None:
    for candidate in ("index", "home"):
        if candidate in page_map:
            return candidate
    configured = str(home_page_name(layout_dir) or "").strip()
    return configured if configured in page_map else None


def referenced_pages(path: Path) -> list[str]:
    if not path.exists():
        return []
    data = load_yaml(path)
    buttons = data.get("buttons")
    if not isinstance(buttons, list):
        return []
    pages: list[str] = []
    seen: set[str] = set()
    for button in buttons:
        if not isinstance(button, dict):
            continue
        if str(button.get("type") or "").strip() != "page":
            continue
        page_name = str(button.get("page") or "").strip()
        if not page_name or page_name in seen:
            continue
        pages.append(page_name)
        seen.add(page_name)
    return pages


def ordered_page_files(layout_dir: Path, layout_meta: dict[str, Any]) -> list[Path]:
    page_map = {
        path.stem: path
        for path in sorted(layout_dir.glob("*.yaml"))
        if path.name not in {"config.yaml", "pager.yaml", "_docs.yaml"}
    }
    if not page_map:
        return []

    excluded = {
        str(entry).strip()
        for entry in layout_meta.get("exclude_pages", [])
        if str(entry).strip()
    }
    ordered_names: list[str] = []
    seen: set[str] = set()

    def add_name(name: str) -> None:
        if not name or name in seen or name not in page_map or name in excluded:
            return
        ordered_names.append(name)
        seen.add(name)

    entry_page = docs_entry_page_name(layout_dir, page_map)
    pager_path = layout_dir / "pager.yaml"

    if not pager_path.exists():
        add_name(str(entry_page or "").strip())

    for name in referenced_pages(pager_path):
        add_name(name)

    home_page = str(entry_page or "").strip()
    if home_page and home_page in page_map:
        for name in referenced_pages(page_map[home_page]):
            add_name(name)

    for name in sorted(page_map):
        add_name(name)

    return [page_map[name] for name in ordered_names]


def aircraft_title(slug: str, config: dict[str, Any]) -> str:
    return str(config.get("aircraft") or config.get("model") or titleize_slug(slug))


def decktype_catalog() -> dict[str, Path]:
    catalog: dict[str, Path] = {}
    for path in sorted(DECKTYPES_DIR.glob("*.yaml")):
        data = load_yaml(path)
        name = str(data.get("name") or data.get("type") or "").strip()
        if name:
            catalog[name] = path
    return catalog


def has_supported_preview_geometry(decktype_path: Path) -> bool:
    decktype = load_yaml(decktype_path)
    buttons = decktype.get("buttons", [])
    if not isinstance(buttons, list):
        return False
    image_buttons = [button for button in buttons if isinstance(button, dict) and button.get("feedback") == "image"]
    grid_button = next((button for button in image_buttons if button.get("name") == 0 and button.get("repeat")), None)
    if grid_button is None:
        return False
    unsupported = [
        button for button in image_buttons if button.get("name") not in {0, "left", "right"}
    ]
    return not unsupported


def pack_layout_docs(pack_meta: dict[str, Any], layout_name: str) -> dict[str, Any]:
    layouts = pack_meta.get("layouts")
    if not isinstance(layouts, list):
        return {}
    for entry in layouts:
        if not isinstance(entry, dict):
            continue
        if str(entry.get("id") or "").strip() != layout_name:
            continue
        return {
            key: value
            for key, value in entry.items()
            if key != "id"
        }
    return {}


def load_layout_docs(layout_dir: Path, pack_meta: dict[str, Any] | None = None) -> dict[str, Any]:
    """Load layout doc metadata from manifest.yaml first, then legacy _docs.yaml."""
    if pack_meta:
        from_pack = pack_layout_docs(pack_meta, layout_dir.name)
        if from_pack:
            return from_pack
    docs_path = layout_dir / "_docs.yaml"
    if not docs_path.exists():
        return {}
    return load_yaml(docs_path)


def layout_entries(config: dict[str, Any], deckconfig_dir: Path, pack_meta: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    decktypes = decktype_catalog()
    entries = config.get("decks", [])
    layouts: list[dict[str, Any]] = []
    if isinstance(entries, list):
        for entry in entries:
            if not isinstance(entry, dict):
                continue
            layout_name = str(entry.get("layout", "")).strip()
            if not layout_name:
                continue
            layout_dir = deckconfig_dir / layout_name
            layout_meta = layout_docs_metadata(layout_dir)
            layout_docs = load_layout_docs(layout_dir, pack_meta=pack_meta)
            page_files = ordered_page_files(layout_dir, layout_meta) if layout_dir.exists() else []
            deck_type = str(entry.get("type") or "").strip()
            decktype_path = decktypes.get(deck_type)
            layouts.append(
                {
                    "name": str(entry.get("name") or layout_name),
                    "type": deck_type,
                    "decktype_path": decktype_path,
                    "layout": layout_name,
                    "dir": layout_dir,
                    "pages": page_files,
                    "docs": layout_meta,
                    "layout_docs": layout_docs,
                    "title": humanize_deck_type(deck_type) if deck_type else str(entry.get("name") or layout_name),
                }
            )
    return layouts


def page_title(page_path: Path) -> str:
    page = load_yaml(page_path)
    docs = normalize_docs_metadata(page.get("_docs") or page.get("docs"))
    stem = page_path.stem

    doc_title = docs.get("title")
    if doc_title is not None and str(doc_title).strip():
        return str(doc_title).strip()

    desc = page.get("description")
    if desc is not None:
        cleaned = _clean_description(str(desc))
        if cleaned:
            return cleaned

    name = page.get("name")
    if name is not None and str(name).strip():
        name_s = str(name).strip()
        if name_s != stem:
            return name_s

    if stem in PAGE_NAME_OVERRIDES:
        return PAGE_NAME_OVERRIDES[stem]

    return titleize_slug(stem.replace("_", "-"))



def page_image_path(slug: str, page_path: Path) -> Path | None:
    image_dir = IMAGE_ROOT / slug
    for suffix in (".png", ".jpg", ".jpeg", ".webp"):
        candidate = image_dir / f"{page_path.stem}{suffix}"
        if candidate.exists():
            return candidate
    return None


def render_layout_page_images(slug: str, layout: dict[str, Any]) -> dict[Path, Path]:
    if not RENDER_PREVIEW_SCRIPT.exists():
        return {}

    preview_mode = str(layout["docs"].get("preview") or "").strip().lower()
    decktype_path = layout.get("decktype_path")
    if preview_mode in {"none", "off", "static"}:
        return {}
    if decktype_path is None or not has_supported_preview_geometry(decktype_path):
        return {}

    output_dir = IMAGE_ROOT / slug / "generated" / layout["layout"]
    output_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix=f"{slug}-{layout['layout']}-") as temp_dir:
        temp_image_dir = Path(temp_dir)
        render_args = [
            "python3",
            str(RENDER_PREVIEW_SCRIPT),
            "--layout-dir",
            str(layout["dir"]),
            "--decktype",
            str(decktype_path),
            "--output-dir",
            str(temp_image_dir),
        ]
        fixture = resolve_repo_path(layout["docs"].get("fixture"), base_dir=layout["dir"])
        if fixture is not None:
            render_args.extend(["--fixture", str(fixture)])
        for page_path in layout["pages"]:
            render_args.extend(["--page", page_path.stem])
        run(render_args)

        expected_images: dict[Path, Path] = {}
        expected_names: set[str] = set()
        for page_path in layout["pages"]:
            source = temp_image_dir / f"{page_path.stem}.png"
            target = output_dir / f"{page_path.stem}.page.png"
            write_bytes_if_changed(target, source.read_bytes())
            expected_images[page_path] = target
            expected_names.add(target.name)

    for stale in output_dir.glob("*.page.png"):
        if stale.name not in expected_names:
            stale.unlink()

    return expected_images



def render_layout_page_svgs(slug: str, layout: dict[str, Any]) -> dict[Path, Path]:
    """Render interactive SVG previews for each page in a layout.

    Returns {page_path: svg_path} for every page that was successfully rendered.
    Falls back gracefully if SVGRenderer is not available or the decktype is unsupported.
    """
    if not _SVG_RENDERER_AVAILABLE:
        return {}
    decktype_path = layout.get("decktype_path")
    if decktype_path is None or not has_supported_preview_geometry(decktype_path):
        return {}

    output_dir = IMAGE_ROOT / slug / "generated" / layout["layout"]
    output_dir.mkdir(parents=True, exist_ok=True)

    fixture = resolve_repo_path(layout["docs"].get("fixture"), base_dir=layout["dir"])
    renderer = SVGRenderer(
        layout_dir=layout["dir"],
        decktype_path=decktype_path,
        fixture_path=fixture,
        repo_blob_url_fn=repo_blob_url,
    )

    result: dict[Path, Path] = {}
    for page_path in layout["pages"]:
        target = output_dir / f"{page_path.stem}.page.svg"
        try:
            renderer.render_page(page_path.stem, target)
            result[page_path] = target
        except Exception:
            pass
    return result


STATUS_LABEL = {
    "stable": "Stable",
    "active": "Active Development",
    "wip": "Work in Progress",
}

STATUS_ICON = {
    "stable": "\u2705",       # ✅
    "active": "\U0001f527",   # 🔧
    "wip": "\U0001f6a7",      # 🚧
}


def build_pack_meta_section(pack_meta: dict[str, Any]) -> list[str]:
    """Render top-of-page metadata block from manifest.yaml fields."""
    if not pack_meta:
        return []

    lines: list[str] = []

    # Metadata pill row
    meta_items: list[str] = []

    icao = str(pack_meta.get("icao") or "").strip()
    if icao:
        meta_items.append(f"\u2708\ufe0f&nbsp;<strong>{icao}</strong>")

    version = pack_meta.get("version")
    if version is not None:
        ver_str = str(version).strip()
        if ver_str and not ver_str.startswith("v"):
            ver_str = f"v{ver_str}"
        if ver_str:
            meta_items.append(f"\U0001f3f7&nbsp;{ver_str}")

    status = str(pack_meta.get("status") or "").strip()
    if status and status in STATUS_LABEL:
        icon = STATUS_ICON.get(status, "")
        label = STATUS_LABEL[status]
        meta_items.append(f"{icon}&nbsp;<strong>{label}</strong>")

    if meta_items:
        lines.append(f'<div class="pack-meta">{"&emsp;".join(meta_items)}</div>')
        lines.append("")

    description = str(pack_meta.get("description") or "").strip()
    if description:
        lines.append(description)
        lines.append("")

    summary = str(pack_meta.get("summary") or "").strip()
    if summary:
        lines.append(f"*{summary}*")
        lines.append("")

    requires = pack_meta.get("requires")
    if isinstance(requires, list) and requires:
        req_str = ", ".join(f"`{REQUIRES_LABELS.get(r, r)}`" for r in requires if str(r).strip())
        if req_str:
            lines.append(f"**Requires:** {req_str}")
            lines.append("")

    return lines


def build_overview(slug: str, config: dict[str, Any], doc_path: Path, page_images: dict[str, dict[Path, Path]], page_svgs: dict[str, dict[Path, Path]] | None = None) -> str:
    deckconfig_dir = DECKS_DIR / slug / "deckconfig"
    title = aircraft_title(slug, config)
    pack_meta = load_pack_metadata(slug)
    layouts = layout_entries(config, deckconfig_dir, pack_meta=pack_meta)

    lines = [
        f"# {title}",
        "",
        '??? note "Auto-generated"',
        "    This page is generated by `scripts/generate_deck_docs.py` — do not edit directly.",
        "",
    ]
    lines.extend(build_pack_meta_section(pack_meta))
    if layouts:
        for layout in layouts:
            page_count = len(layout["pages"])
            layout_docs = layout["layout_docs"]
            status = str(layout_docs.get("status") or "").strip()
            deck_type = layout["type"]

            lines.append(f"## {layout['title']}")
            lines.append("")

            # Metadata bar
            meta_items: list[str] = []
            if status and status in STATUS_LABEL:
                icon = STATUS_ICON.get(status, "")
                label = STATUS_LABEL[status]
                meta_items.append(f'{icon} <strong>{label}</strong>')
            meta_items.append(f'\U0001f4c4 {page_count} page{"s" if page_count != 1 else ""}')
            if deck_type:
                meta_items.append(f'\U0001f3ae {humanize_deck_type(deck_type)}')
            version = layout_docs.get("version")
            if version is not None:
                ver_str = str(version).strip()
                if ver_str and not ver_str.startswith("v"):
                    ver_str = f"v{ver_str}"
                if ver_str:
                    meta_items.append(f'\U0001f3f7 {ver_str}')

            # Optional mini progress bar inside the panel
            progress_html = ""
            progress = layout_docs.get("progress")
            if progress is not None:
                try:
                    pct = max(0, min(100, int(progress)))
                except (TypeError, ValueError):
                    pct = 0
                progress_html = (
                    f'<div class="layout-progress-mini" title="Completion: {pct}%">'
                    f'<div class="layout-progress-track"><div class="layout-progress-bar" style="width: {pct}%"></div></div>'
                    f'<span class="layout-progress-label">{pct}%</span></div>'
                )

            meta_content = f'<div class="layout-meta-items">{"&emsp;".join(meta_items)}</div>'
            if progress_html:
                meta_content += progress_html
            lines.append(f'<div class="layout-meta">{meta_content}</div>')
            lines.append("")

            # Optional layout summary
            summary = str(layout_docs.get("summary") or "").strip()
            if summary:
                lines.append(summary)
                lines.append("")

            # Issues and planned (MkDocs admonitions)
            issues = layout_docs.get("issues")
            planned = layout_docs.get("planned")
            if isinstance(issues, list) and issues:
                lines.append('!!! warning "Known issues"')
                for item in issues:
                    lines.append(f"    - {item}")
                lines.append("")
            if isinstance(planned, list) and planned:
                lines.append('!!! info "Planned"')
                for item in planned:
                    lines.append(f"    - {item}")
                lines.append("")

            images = page_images.get(layout["layout"], {})
            svgs = (page_svgs or {}).get(layout["layout"], {})
            if layout["pages"]:
                lines.append('<div class="page-gallery">')
                for page_path in layout["pages"]:
                    name = page_title(page_path)
                    image_path = images.get(page_path)
                    svg_path = svgs.get(page_path)
                    config_url = repo_blob_url(page_path)
                    lines.append('<div class="page-card">')
                    if svg_path:
                        svg_ref = rel_path(svg_path, doc_path)
                        # Extract width/height from the SVG so <object> renders at the right size.
                        # <object> renders SVG interactively (hover tooltips, clickable links).
                        svg_dims = _svg_dimensions(svg_path)
                        dim_attr = f' style="width:100%;max-width:{svg_dims[0]}px;aspect-ratio:{svg_dims[0]}/{svg_dims[1]}"' if svg_dims else ""
                        lines.append(f'<object type="image/svg+xml" data="{svg_ref}" title="{name}"{dim_attr}>')
                        if image_path:
                            image_ref = rel_path(image_path, doc_path)
                            lines.append(f'<img src="{image_ref}" alt="{name} preview" loading="lazy">')
                        lines.append('</object>')
                    elif image_path:
                        image_ref = rel_path(image_path, doc_path)
                        lines.append(f'<a href="{image_ref}" data-glightbox data-title="{name}">')
                        lines.append(f'<img src="{image_ref}" alt="{name} preview" loading="lazy">')
                        lines.append('</a>')
                    lines.append(f'<div class="page-name">{name}</div>')
                    lines.append(f'<div class="page-config"><a href="{config_url}">{page_path.name}</a></div>')
                    lines.append('</div>')
                lines.append('</div>')
                lines.append("")
    else:
        lines.append("No layout metadata found.")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def format_nav_yaml(aircraft_records: list[dict[str, Any]]) -> str:
    """Build the Decks nav section as YAML text (aircraft-only, no layout children)."""
    lines: list[str] = []
    for record in aircraft_records:
        slug = record["slug"]
        title = record["title"]
        lines.append(f"      - {title}: decks/{slug}/index.md")
    return "\n".join(lines)


def update_mkdocs_nav(aircraft_records: list[dict[str, Any]]) -> None:
    if not MKDOCS_CONFIG.exists():
        return
    text = MKDOCS_CONFIG.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    # Find the "  - Decks:" line and the next sibling at same indent
    decks_start = None
    decks_end = None
    for idx, line in enumerate(lines):
        stripped = line.rstrip()
        if stripped == "- Decks:" and line.lstrip() == "- Decks:\n" or line.rstrip() == "  - Decks:":
            decks_start = idx
        elif decks_start is not None and idx > decks_start:
            # Next top-level nav entry (same indent as "  - Decks:")
            if line.startswith("  - ") and not line.startswith("      "):
                decks_end = idx
                break
    if decks_start is None:
        return
    if decks_end is None:
        # Decks is the last nav section; find end of nav block
        for idx in range(decks_start + 1, len(lines)):
            if lines[idx] and not lines[idx][0].isspace():
                decks_end = idx
                break
        if decks_end is None:
            decks_end = len(lines)

    nav_text = "  - Decks:\n" + format_nav_yaml(aircraft_records) + "\n"
    new_text = "".join(lines[:decks_start]) + nav_text + "".join(lines[decks_end:])
    write_text_if_changed(MKDOCS_CONFIG, new_text)


def render_all_images(slug: str, config: dict[str, Any], deckconfig_dir: Path) -> tuple[dict[str, dict[Path, Path]], dict[str, dict[Path, Path]]]:
    """Render preview images and SVGs for all layouts.

    Returns (png_map, svg_map) where each map is {layout_name: {page_path: file_path}}.
    """
    all_images: dict[str, dict[Path, Path]] = {}
    all_svgs: dict[str, dict[Path, Path]] = {}
    for layout in layout_entries(config, deckconfig_dir):
        if not layout["pages"]:
            continue
        images = render_layout_page_images(slug, layout)
        if not images:
            for page_path in layout["pages"]:
                image_path = page_image_path(slug, page_path)
                if image_path is None:
                    images = {}
                    break
                images[page_path] = image_path
        if images:
            all_images[layout["layout"]] = images
        svgs = render_layout_page_svgs(slug, layout)
        if svgs:
            all_svgs[layout["layout"]] = svgs
    return all_images, all_svgs


def main() -> int:
    DOCS_DECKS_DIR.mkdir(parents=True, exist_ok=True)

    aircraft_records: list[dict[str, Any]] = []
    for aircraft_dir in sorted(path for path in DECKS_DIR.iterdir() if path.is_dir()):
        deckconfig_dir = aircraft_dir / "deckconfig"
        config_path = deckconfig_dir / "config.yaml"
        if not config_path.exists():
            continue

        slug = aircraft_dir.name
        config = load_yaml(config_path)
        page_images, page_svgs = render_all_images(slug, config, deckconfig_dir)
        doc_path = DOCS_DECKS_DIR / slug / "index.md"
        doc_path.parent.mkdir(parents=True, exist_ok=True)
        write_text_if_changed(doc_path, build_overview(slug, config, doc_path, page_images, page_svgs))

        title = aircraft_title(slug, config)
        aircraft_records.append({"slug": slug, "title": title})

    update_mkdocs_nav(aircraft_records)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
