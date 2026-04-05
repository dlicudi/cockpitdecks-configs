#!/usr/bin/env python3
"""Build configs.json for the Cockpitdecks config browser.

Walks all aircraft deckconfig directories, compiles each deck's YAML
configuration to JSON via SVGRenderer.yaml_to_json(), and writes a single
docs/assets/configs.json.  Also copies deck-render.js and any required font
files to the docs/assets tree.

Usage:
    python scripts/build_configs_json.py
"""

from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

from generate_deck_docs import (
    aircraft_title,
    has_supported_preview_geometry,
    home_page_name,
    layout_entries,
    load_pack_metadata,
    load_yaml,
    page_title,
    resolve_repo_path,
)
from render_deck_preview import FONT_DIRS, SVGRenderer

ROOT       = Path(__file__).resolve().parents[1]
DECKS_DIR  = ROOT / "decks"
DOCS_DIR   = ROOT / "docs"
ASSETS_DIR = DOCS_DIR / "assets"
FONTS_DIR  = ASSETS_DIR / "fonts"
JS_DIR     = ASSETS_DIR / "js"

DECK_RENDER_JS = Path(__file__).parent / "deck-render.js"


# ── Font handling ──────────────────────────────────────────────────────────────

def _build_font_catalog() -> dict[str, tuple[Path, str]]:
    """Return {filename: (path, css_family)} for every font file found."""
    alias = SVGRenderer._FONT_ALIAS  # {config_name: (filename, css_family)}
    # Invert to filename → css_family (de-duplicated)
    file_to_family: dict[str, str] = {}
    for _cfg_name, (filename, family) in alias.items():
        file_to_family.setdefault(filename, family)

    catalog: dict[str, tuple[Path, str]] = {}
    for filename, family in file_to_family.items():
        for d in FONT_DIRS:
            candidate = d / filename
            if candidate.exists():
                catalog[filename] = (candidate, family)
                break
    return catalog


def copy_fonts(font_names: set[str], catalog: dict[str, tuple[Path, str]]) -> dict[str, str]:
    """Copy needed font files to FONTS_DIR.  Returns {filename: css_family}."""
    FONTS_DIR.mkdir(parents=True, exist_ok=True)
    alias = SVGRenderer._FONT_ALIAS
    result: dict[str, str] = {}

    for name in font_names:
        info = alias.get(name)
        if not info:
            lower = name.lower()
            for k, v in alias.items():
                if k.lower() == lower or v[0].lower() == lower:
                    info = v
                    break
        if not info:
            continue
        filename, family = info
        if filename in result:
            continue
        entry = catalog.get(filename)
        if not entry:
            continue
        src_path, _ = entry
        dst = FONTS_DIR / filename
        if not dst.exists() or dst.stat().st_mtime < src_path.stat().st_mtime:
            shutil.copy2(src_path, dst)
        result[filename] = family

    return result


# ── JSON generation ────────────────────────────────────────────────────────────

def build_deck_entry(
    layout: dict[str, Any],
    font_catalog: dict[str, tuple[Path, str]],
    all_font_names: set[str],
) -> dict[str, Any] | None:
    decktype_path = layout.get("decktype_path")
    if decktype_path is None or not has_supported_preview_geometry(decktype_path):
        return None
    if not layout["pages"]:
        return None

    layout_dir = layout["dir"]
    fixture    = resolve_repo_path(layout["docs"].get("fixture"), base_dir=layout_dir)

    try:
        renderer   = SVGRenderer(layout_dir=layout_dir, decktype_path=decktype_path, fixture_path=fixture)
        page_names = [p.stem for p in layout["pages"]]
        config     = renderer.yaml_to_json(page_names)
    except Exception as e:
        print(f"    yaml_to_json failed: {e}")
        return None

    # Collect font names for this deck
    font_names: set[str] = renderer._collect_font_names(config["pages"])
    # Always include the standard display fonts
    font_names.update({"Segment7Standard.otf", "D-DIN-Bold.otf", "D-DINCondensed.otf"})
    all_font_names.update(font_names)

    # Resolve filename → CSS family pairs actually available on disk
    alias = SVGRenderer._FONT_ALIAS
    deck_fonts: list[dict[str, str]] = []
    seen_files: set[str] = set()
    for name in sorted(font_names):
        info = alias.get(name)
        if not info:
            lower = name.lower()
            for k, v in alias.items():
                if k.lower() == lower or v[0].lower() == lower:
                    info = v
                    break
        if not info:
            continue
        filename, family = info
        if filename in seen_files:
            continue
        seen_files.add(filename)
        if filename in font_catalog:
            deck_fonts.append({"file": filename, "family": family})

    home = home_page_name(layout_dir) or (page_names[0] if page_names else "index")
    pages_meta = [{"name": p.stem, "title": page_title(p)} for p in layout["pages"]]

    return {
        "id":        layout["layout"],
        "title":     layout["title"],
        "type":      layout["type"],
        "home_page": home,
        "fonts":     deck_fonts,
        "pages":     pages_meta,
        "config":    config,
    }


def build_aircraft_entry(
    aircraft_dir: Path,
    font_catalog: dict[str, tuple[Path, str]],
    all_font_names: set[str],
) -> dict[str, Any] | None:
    deckconfig_dir = aircraft_dir / "deckconfig"
    config_path    = deckconfig_dir / "config.yaml"
    if not config_path.exists():
        return None

    slug       = aircraft_dir.name
    config     = load_yaml(config_path)
    title      = aircraft_title(slug, config)
    pack_meta  = load_pack_metadata(slug)
    layouts    = layout_entries(config, deckconfig_dir, pack_meta=pack_meta)

    decks: list[dict[str, Any]] = []
    for layout in layouts:
        entry = build_deck_entry(layout, font_catalog, all_font_names)
        if entry:
            decks.append(entry)

    if not decks:
        return None

    return {"slug": slug, "title": title, "decks": decks}


# ── Entry point ────────────────────────────────────────────────────────────────

def main() -> int:
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    JS_DIR.mkdir(parents=True, exist_ok=True)

    # Copy deck-render.js
    if DECK_RENDER_JS.exists():
        dst = JS_DIR / "deck-render.js"
        if not dst.exists() or dst.stat().st_mtime < DECK_RENDER_JS.stat().st_mtime:
            shutil.copy2(DECK_RENDER_JS, dst)
            print(f"Copied deck-render.js → {dst.relative_to(ROOT)}")

    font_catalog   = _build_font_catalog()
    all_font_names: set[str] = set()
    aircraft_list: list[dict[str, Any]] = []

    for aircraft_dir in sorted(p for p in DECKS_DIR.iterdir() if p.is_dir()):
        slug = aircraft_dir.name
        print(f"  {slug}", end=" ", flush=True)
        entry = build_aircraft_entry(aircraft_dir, font_catalog, all_font_names)
        if entry:
            aircraft_list.append(entry)
            print(f"→ {len(entry['decks'])} deck(s)")
        else:
            print("(skipped)")

    # Copy font files
    copied = copy_fonts(all_font_names, font_catalog)
    print(f"\nFonts: {len(copied)} files copied to {FONTS_DIR.relative_to(ROOT)}")

    output = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "aircraft":  aircraft_list,
    }
    output_path = ASSETS_DIR / "configs.json"
    with open(output_path, "w", encoding="utf-8") as fp:
        json.dump(output, fp, ensure_ascii=False, separators=(",", ":"))

    size_kb = output_path.stat().st_size // 1024
    print(f"Written {output_path.relative_to(ROOT)} ({size_kb} KB, {len(aircraft_list)} aircraft)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
