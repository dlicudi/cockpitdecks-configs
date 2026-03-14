#!/usr/bin/env python3
"""Regenerate deck overview docs from config."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any
import os

import yaml


ROOT = Path(__file__).resolve().parents[1]
DECKS_DIR = ROOT / "decks"
DOCS_DECKS_DIR = ROOT / "docs" / "decks"
IMAGE_ROOT = ROOT / "docs" / "assets" / "images"
SR22_SCRIPT = ROOT / "scripts" / "generate_sr22_docs.py"

PAGE_NAME_OVERRIDES = {
    "index": "Home",
    "pfi": "PFI",
    "fcu": "FCU",
    "gcu478": "GCU478",
}

DOC_PATH_OVERRIDES = {
    "toliss-airbus-a320-neo": "toliss-airbus-A320-neo.md",
    "toliss-airbus-a321-neo": "toliss-airbus-A321-neo.md",
}


def run(args: list[str]) -> None:
    subprocess.run(args, check=True, cwd=ROOT)


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return data


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


def doc_filename(slug: str) -> str:
    return DOC_PATH_OVERRIDES.get(slug, f"{slug}.md")


def rel_image_path(path: Path, doc_path: Path) -> str:
    return os.path.relpath(path, doc_path.parent).replace("\\", "/")


def built_page_asset_path(path: Path, doc_path: Path) -> str:
    rel_to_docs = path.relative_to(ROOT / "docs")
    rel_doc = doc_path.relative_to(ROOT / "docs")
    depth = len(rel_doc.parent.parts) + (0 if rel_doc.name == "index.md" else 1)
    return "../" * depth + str(rel_to_docs).replace("\\", "/")


def resolve_docs_image(ref: str) -> Path | None:
    cleaned = ref.strip()
    if not cleaned:
        return None
    marker = "assets/"
    if marker in cleaned:
        suffix = cleaned[cleaned.index(marker) :]
        candidate = ROOT / "docs" / suffix
        return candidate if candidate.exists() else None
    candidate = ROOT / "docs" / cleaned.lstrip("./")
    return candidate if candidate.exists() else None


def first_image(slug: str) -> Path | None:
    image_dir = IMAGE_ROOT / slug
    if not image_dir.exists():
        fallback = IMAGE_ROOT / "Loupedeck_live.png"
        return fallback if fallback.exists() else None

    candidates = [
        image_dir / f"{slug}.png",
        image_dir / f"{slug}.jpg",
        image_dir / f"{slug}.jpeg",
        image_dir / f"{slug}-banner.jpg",
        image_dir / f"{slug}-banner.png",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    for candidate in sorted(image_dir.iterdir()):
        if candidate.is_file() and candidate.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"} and "generated" not in candidate.parts:
            return candidate

    fallback = IMAGE_ROOT / "Loupedeck_live.png"
    return fallback if fallback.exists() else None


def normalize_docs_metadata(meta: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(meta, dict):
        return {}
    return meta


def layout_entries(config: dict[str, Any], deckconfig_dir: Path) -> list[dict[str, Any]]:
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
            page_files = []
            if layout_dir.exists():
                page_files = [path for path in sorted(layout_dir.glob("*.yaml")) if path.name not in {"config.yaml", "pager.yaml"}]
            deck_type = str(entry.get("type") or "").strip()
            layouts.append(
                {
                    "name": str(entry.get("name") or layout_name),
                    "type": deck_type,
                    "layout": layout_name,
                    "dir": layout_dir,
                    "pages": page_files,
                    "title": humanize_deck_type(deck_type) if deck_type else str(entry.get("name") or layout_name),
                }
            )
    return layouts


def page_title(page_path: Path) -> str:
    page = load_yaml(page_path)
    docs = normalize_docs_metadata(page.get("_docs") or page.get("docs"))
    title = str(docs.get("title") or page.get("description") or page.get("name") or page_path.stem)
    if page_path.stem in PAGE_NAME_OVERRIDES:
        return PAGE_NAME_OVERRIDES[page_path.stem]
    return title if title != page_path.stem else titleize_slug(title.replace("_", "-"))


def build_overview(slug: str, config: dict[str, Any], docs_meta: dict[str, Any], doc_path: Path) -> str:
    aircraft_meta = normalize_docs_metadata(docs_meta.get("aircraft"))
    deckconfig_dir = DECKS_DIR / slug / "deckconfig"
    title = str(aircraft_meta.get("title") or config.get("model") or config.get("aircraft") or titleize_slug(slug))
    summary = str(aircraft_meta.get("summary") or config.get("description") or f"Deck definitions for {title}.")
    eyebrow = str(aircraft_meta.get("eyebrow") or "")
    tags = aircraft_meta.get("tags", [])
    if not isinstance(tags, list):
        tags = []
    icon = str(aircraft_meta.get("icon") or "material/airplane")

    hero_image = aircraft_meta.get("hero_image")
    if hero_image:
        hero_path = resolve_docs_image(str(hero_image))
    else:
        hero_path = first_image(slug)
    hero_src = built_page_asset_path(hero_path, doc_path) if hero_path and hero_path.exists() else ""
    hero_alt = str(aircraft_meta.get("hero_alt") or title)

    layouts = layout_entries(config, deckconfig_dir)

    lines = [
        "---",
        f"icon: {icon}",
        "---",
        "",
        f"# {title}",
        "",
        '<div class="cdx-hero cdx-hero--compact">',
        '  <div class="cdx-hero__copy">',
    ]
    if eyebrow:
        lines.append(f'    <p class="cdx-eyebrow">{eyebrow}</p>')
    lines.extend(
        [
            f"    <h1>{title}</h1>",
            '    <p class="cdx-lead">',
            f"      {summary}",
            "    </p>",
        ]
    )
    if tags:
        tag_html = " ".join(f"<code>{tag}</code>" for tag in tags)
        lines.append(f"    <p>{tag_html}</p>")
    lines.extend(["  </div>", '  <div class="cdx-hero__visual">'])
    if hero_src:
        lines.append(f'    <img src="{hero_src}" alt="{hero_alt}" />')
    lines.extend(["  </div>", "</div>", "", "## Layouts", ""])

    if layouts:
        lines.append('<div class="cdx-grid cdx-grid--cards">')
        for layout in layouts:
            layout_doc = ROOT / "docs" / "decks" / slug / layout["layout"] / "index.md"
            href = f"{layout['layout']}/" if layout_doc.exists() else "#"
            page_count = len(layout["pages"])
            summary = f"`{layout['type']}` layout with {page_count} page{'s' if page_count != 1 else ''}."
            lines.extend(
                [
                    f'  <a class="cdx-card" href="{href}">',
                    '    <div class="cdx-card__body">',
                    f'      <h3>{layout["title"]}</h3>',
                    f'      <p>{summary}</p>',
                    "    </div>",
                    "  </a>",
                ]
            )
        lines.append("</div>")
    else:
        lines.append("- No layout metadata found.")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def build_index(aircraft_entries: list[dict[str, str]]) -> str:
    lines = [
        "<!-- generated by scripts/generate_deck_docs.py; do not edit directly -->",
        "",
        "# Decks",
        "",
        "Browse the available config-driven deck docs.",
        "",
        '<div class="cdx-grid cdx-grid--cards">',
    ]
    for entry in aircraft_entries:
        lines.extend(
            [
                f'  <a class="cdx-card" href="{entry["href"]}">',
                f'    <img src="{entry["image"]}" alt="{entry["title"]}" />',
                '    <div class="cdx-card__body">',
                f'      <h3>{entry["title"]}</h3>',
                f'      <p>{entry["summary"]}</p>',
                "    </div>",
                "  </a>",
            ]
        )
    lines.extend(["</div>", ""])
    return "\n".join(lines)


def main() -> int:
    DOCS_DECKS_DIR.mkdir(parents=True, exist_ok=True)

    if SR22_SCRIPT.exists():
        run(["python3", str(SR22_SCRIPT)])

    aircraft_entries: list[dict[str, str]] = []
    for aircraft_dir in sorted(path for path in DECKS_DIR.iterdir() if path.is_dir()):
        deckconfig_dir = aircraft_dir / "deckconfig"
        config_path = deckconfig_dir / "config.yaml"
        if not config_path.exists():
            continue

        slug = aircraft_dir.name
        config = load_yaml(config_path)
        docs_meta = load_yaml(deckconfig_dir / "_docs.yaml") if (deckconfig_dir / "_docs.yaml").exists() else {}
        doc_path = DOCS_DECKS_DIR / doc_filename(slug)
        doc_path.write_text(build_overview(slug, config, docs_meta, doc_path), encoding="utf-8")

        aircraft_meta = normalize_docs_metadata(docs_meta.get("aircraft"))
        title = str(aircraft_meta.get("title") or config.get("model") or config.get("aircraft") or titleize_slug(slug))
        summary = str(aircraft_meta.get("summary") or config.get("description") or f"Deck definitions for {title}.")
        image_path = aircraft_meta.get("hero_image")
        if image_path:
            image = resolve_docs_image(str(image_path))
        else:
            image = first_image(slug)
        if image and image.exists():
            image_ref = built_page_asset_path(image, DOCS_DECKS_DIR / "index.md")
        else:
            image_ref = "../assets/images/Loupedeck_live.png"
        aircraft_entries.append(
            {
                "href": doc_filename(slug).replace(".md", "/"),
                "image": image_ref,
                "title": title,
                "summary": summary,
            }
        )

    (DOCS_DECKS_DIR / "index.md").write_text(build_index(aircraft_entries), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
