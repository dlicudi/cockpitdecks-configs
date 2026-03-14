#!/usr/bin/env python3
"""Regenerate deck overview docs from config."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any
import os
import tempfile

import yaml


ROOT = Path(__file__).resolve().parents[1]
DECKS_DIR = ROOT / "decks"
DOCS_DECKS_DIR = ROOT / "docs" / "decks"
IMAGE_ROOT = ROOT / "docs" / "assets" / "images"
RENDER_PREVIEW_SCRIPT = ROOT / "scripts" / "render_deck_preview.py"
REPO_BLOB_BASE = "https://github.com/dlicudi/cockpitdecks-configs/blob/main"

PAGE_NAME_OVERRIDES = {
    "audiopanel": "Audio Panel",
    "home": "Home",
    "index": "Home",
    "pfi": "PFI",
    "fcu": "FCU",
    "g1000": "G1000",
    "gcu478": "GCU478",
    "switches": "Switches",
    "switches2": "Switches 2",
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


def repo_blob_url(path: Path) -> str:
    return f"{REPO_BLOB_BASE}/{path.relative_to(ROOT).as_posix()}"


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


def resolve_repo_path(value: str | Path | None) -> Path | None:
    if value is None:
        return None
    candidate = Path(str(value))
    if candidate.is_absolute():
        return candidate
    return ROOT / candidate


def layout_docs_metadata(docs_meta: dict[str, Any], layout_name: str) -> dict[str, Any]:
    layouts = docs_meta.get("layouts")
    if not isinstance(layouts, dict):
        return {}
    meta = layouts.get(layout_name)
    return meta if isinstance(meta, dict) else {}


def ordered_page_files(layout_dir: Path, layout_meta: dict[str, Any]) -> list[Path]:
    page_map = {
        path.stem: path
        for path in sorted(layout_dir.glob("*.yaml"))
        if path.name not in {"config.yaml", "pager.yaml"}
    }
    if not page_map:
        return []

    ordered_names = layout_meta.get("pages")
    if isinstance(ordered_names, list):
        ordered: list[Path] = []
        seen: set[str] = set()
        for entry in ordered_names:
            name = str(entry).strip()
            if not name or name in seen or name not in page_map:
                continue
            ordered.append(page_map[name])
            seen.add(name)
        return ordered

    excluded = {
        str(entry).strip()
        for entry in layout_meta.get("exclude_pages", [])
        if str(entry).strip()
    }
    return [path for name, path in page_map.items() if name not in excluded]


def aircraft_title(slug: str, config: dict[str, Any], docs_meta: dict[str, Any]) -> str:
    aircraft_meta = normalize_docs_metadata(docs_meta.get("aircraft"))
    return str(aircraft_meta.get("title") or config.get("model") or config.get("aircraft") or titleize_slug(slug))


def layout_entries(config: dict[str, Any], deckconfig_dir: Path, docs_meta: dict[str, Any]) -> list[dict[str, Any]]:
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
            layout_meta = layout_docs_metadata(docs_meta, layout_name)
            page_files = ordered_page_files(layout_dir, layout_meta) if layout_dir.exists() else []
            deck_type = str(entry.get("type") or "").strip()
            layouts.append(
                {
                    "name": str(entry.get("name") or layout_name),
                    "type": deck_type,
                    "layout": layout_name,
                    "dir": layout_dir,
                    "pages": page_files,
                    "docs": layout_meta,
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


def page_doc_stem(page_path: Path) -> str:
    return "home" if page_path.stem == "index" else page_path.stem


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
    if preview_mode != "generated":
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
            "--output-dir",
            str(temp_image_dir),
        ]
        fixture = resolve_repo_path(layout["docs"].get("fixture"))
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
            target.write_bytes(source.read_bytes())
            expected_images[page_path] = target
            expected_names.add(target.name)

    for stale in output_dir.glob("*.page.png"):
        if stale.name not in expected_names:
            stale.unlink()

    return expected_images


def page_anchor_id(slug: str, layout_name: str, page_name: str) -> str:
    return f"{slug}-{layout_name}-{page_name}-preview"


def build_layout_page(aircraft_title: str, title: str, layout: dict[str, Any], page_docs: list[dict[str, str]]) -> str:
    style = str(layout["docs"].get("style") or "cards").strip().lower()
    lines = [
        "---",
        "icon: material/dialpad",
        "---",
        "",
        "<!-- generated by scripts/generate_deck_docs.py; do not edit directly -->",
        "",
        f"# {title}",
        "",
        f"{title} layout for {aircraft_title}.",
        "",
        "## Pages" if style != "deck-map" else "## Deck Map",
        "",
    ]
    if style == "deck-map":
        lines.append('<div class="cdx-deck">')
        for page in page_docs:
            lines.extend(
                [
                    f'  <a class="cdx-deck__key" href="{page["href"]}" data-preview>',
                    f'    <img src="{page["image"]}" alt="{page["title"]} page preview" />',
                    f'    <span>{page["title"]}</span>',
                    "  </a>",
                ]
            )
        lines.extend(["</div>", ""])
    else:
        lines.append('<div class="cdx-grid cdx-grid--cards">')
        for page in page_docs:
            lines.extend(
                [
                    f'  <a class="cdx-card" href="{page["href"]}">',
                    f'    <img src="{page["image"]}" alt="{page["title"]} page preview" />',
                    '    <div class="cdx-card__body">',
                    f'      <h3>{page["title"]}</h3>',
                    "      <p>Page config and preview.</p>",
                    "    </div>",
                    "  </a>",
                ]
            )
        lines.extend(["</div>", ""])
    return "\n".join(lines)


def build_page_doc(slug: str, layout_name: str, layout_title: str, page_path: Path, image_path: Path) -> str:
    page = load_yaml(page_path)
    page_name = page_path.stem
    title = page_title(page_path)
    doc_stem = page_doc_stem(page_path)
    image_ref = rel_image_path(image_path, DOCS_DECKS_DIR / slug / layout_name / f"{doc_stem}.md")
    includes = [part.strip() for part in str(page.get("includes", "")).split(",") if part.strip()]

    lines = [
        "---",
        f"title: {layout_title} {title}",
        "---",
        "",
        "<!-- generated by scripts/generate_deck_docs.py; do not edit directly -->",
        "",
        f"# {title}",
        "",
        f'<div id="{page_anchor_id(slug, layout_name, page_name)}"></div>',
        "",
        f"![{title} preview]({image_ref})",
        "",
        "## Source",
        "",
        f'[:material-github: `{page_path.parent.name}/{page_path.name}`]({repo_blob_url(page_path)})',
    ]

    if includes:
        include_links: list[str] = []
        for include in includes:
            include_path = page_path.parent / f"{include}.yaml"
            if include_path.exists():
                include_links.append(f'[:material-source-branch: `{include}.yaml`]({repo_blob_url(include_path)})')
            else:
                include_links.append(f"`{include}.yaml`")
        lines.extend(["", "Includes: " + " · ".join(include_links)])

    lines.append("")
    return "\n".join(lines)


def generate_layout_docs(slug: str, config: dict[str, Any], deckconfig_dir: Path, docs_meta: dict[str, Any]) -> None:
    title = aircraft_title(slug, config, docs_meta)
    for layout in layout_entries(config, deckconfig_dir, docs_meta):
        if not layout["pages"]:
            continue

        page_images = render_layout_page_images(slug, layout)
        if not page_images:
            page_images = {}
            for page_path in layout["pages"]:
                image_path = page_image_path(slug, page_path)
                if image_path is None:
                    page_images = {}
                    break
                page_images[page_path] = image_path
        if not page_images:
            continue

        layout_doc_dir = DOCS_DECKS_DIR / slug / layout["layout"]
        layout_doc_dir.mkdir(parents=True, exist_ok=True)

        page_docs: list[dict[str, str]] = []
        for page_path in layout["pages"]:
            page_name = page_path.stem
            doc_stem = page_doc_stem(page_path)
            page_doc_path = layout_doc_dir / f"{doc_stem}.md"
            page_doc_path.write_text(
                build_page_doc(slug, layout["layout"], str(layout["title"]), page_path, page_images[page_path]),
                encoding="utf-8",
            )
            page_docs.append(
                {
                    "title": page_title(page_path),
                    "href": f'{doc_stem}/#{page_anchor_id(slug, layout["layout"], page_name)}',
                    "image": built_page_asset_path(page_images[page_path], layout_doc_dir / "index.md"),
                }
            )

        (layout_doc_dir / "index.md").write_text(
            build_layout_page(title, str(layout["title"]), layout, page_docs),
            encoding="utf-8",
        )


def build_overview(slug: str, config: dict[str, Any], docs_meta: dict[str, Any], doc_path: Path) -> str:
    aircraft_meta = normalize_docs_metadata(docs_meta.get("aircraft"))
    deckconfig_dir = DECKS_DIR / slug / "deckconfig"
    title = aircraft_title(slug, config, docs_meta)
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

    layouts = layout_entries(config, deckconfig_dir, docs_meta)

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

    aircraft_entries: list[dict[str, str]] = []
    for aircraft_dir in sorted(path for path in DECKS_DIR.iterdir() if path.is_dir()):
        deckconfig_dir = aircraft_dir / "deckconfig"
        config_path = deckconfig_dir / "config.yaml"
        if not config_path.exists():
            continue

        slug = aircraft_dir.name
        config = load_yaml(config_path)
        docs_meta = load_yaml(deckconfig_dir / "_docs.yaml") if (deckconfig_dir / "_docs.yaml").exists() else {}
        generate_layout_docs(slug, config, deckconfig_dir, docs_meta)
        doc_path = DOCS_DECKS_DIR / doc_filename(slug)
        doc_path.write_text(build_overview(slug, config, docs_meta, doc_path), encoding="utf-8")

        aircraft_meta = normalize_docs_metadata(docs_meta.get("aircraft"))
        title = aircraft_title(slug, config, docs_meta)
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
