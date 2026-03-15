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
DECKTYPES_DIR = ROOT / "decktypes"
RENDER_PREVIEW_SCRIPT = ROOT / "scripts" / "render_deck_preview.py"
REPO_BLOB_BASE = "https://github.com/dlicudi/cockpitdecks-configs/blob/main"
MKDOCS_CONFIG = ROOT / "mkdocs.yml"

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



def rel_path(target: Path, doc_path: Path) -> str:
    return os.path.relpath(target, doc_path.parent).replace("\\", "/")


def repo_blob_url(path: Path) -> str:
    return f"{REPO_BLOB_BASE}/{path.relative_to(ROOT).as_posix()}"



def normalize_docs_metadata(meta: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(meta, dict):
        return {}
    return meta


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
        if path.name not in {"config.yaml", "pager.yaml"}
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


def aircraft_title(slug: str, config: dict[str, Any], docs_meta: dict[str, Any]) -> str:
    aircraft_meta = normalize_docs_metadata(docs_meta.get("aircraft"))
    return str(aircraft_meta.get("title") or config.get("aircraft") or config.get("model") or titleize_slug(slug))


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


def layout_entries(config: dict[str, Any], deckconfig_dir: Path, docs_meta: dict[str, Any]) -> list[dict[str, Any]]:
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
            target.write_bytes(source.read_bytes())
            expected_images[page_path] = target
            expected_names.add(target.name)

    for stale in output_dir.glob("*.page.png"):
        if stale.name not in expected_names:
            stale.unlink()

    return expected_images



def build_overview(slug: str, config: dict[str, Any], docs_meta: dict[str, Any], doc_path: Path, page_images: dict[str, dict[Path, Path]]) -> str:
    aircraft_meta = normalize_docs_metadata(docs_meta.get("aircraft"))
    deckconfig_dir = DECKS_DIR / slug / "deckconfig"
    title = aircraft_title(slug, config, docs_meta)
    summary = str(aircraft_meta.get("summary") or config.get("description") or f"Deck definitions for {title}.")
    eyebrow = str(aircraft_meta.get("eyebrow") or "")
    tags = aircraft_meta.get("tags", [])
    if not isinstance(tags, list):
        tags = []
    icon = str(aircraft_meta.get("icon") or "material/airplane")

    layouts = layout_entries(config, deckconfig_dir, docs_meta)

    tracking = parse_tracking(docs_meta.get("tracking"))
    state = tracking.get("state", "")

    frontmatter = [
        "---",
        f"icon: {icon}",
    ]
    if tags:
        frontmatter.append(f"tags: [{', '.join(tags)}]")
    if state:
        frontmatter.append(f"status: {state}")
    frontmatter.append("---")

    lines = [
        *frontmatter,
        "",
        "<!-- generated by scripts/generate_deck_docs.py; do not edit directly -->",
        "",
        f"# {title}",
        "",
    ]
    if eyebrow or summary:
        lines.append(f'!!! abstract "{eyebrow}"' if eyebrow else '!!! abstract ""')
        lines.append("")
        if summary:
            lines.append(f"    {summary}")
            lines.append("")
    if layouts:
        use_tabs = len(layouts) > 1
        for layout in layouts:
            page_count = len(layout["pages"])
            layout_label = layout["title"]
            # Indent prefix: 4 spaces inside tabs, none otherwise
            p = "    " if use_tabs else ""
            if use_tabs:
                lines.append(f'=== "{layout_label}"')
            else:
                lines.append(f"## {layout_label}")
            lines.append("")
            lines.append(f"{p}{layout_label} layout with {page_count} page{'s' if page_count != 1 else ''}.")
            lines.append("")
            images = page_images.get(layout["layout"], {})
            if layout["pages"]:
                lines.append(f'{p}<div class="grid cards" markdown>')
                lines.append("")
                for page_path in layout["pages"]:
                    name = page_title(page_path)
                    image_path = images.get(page_path)
                    lines.append(f"{p}-   **{name}**")
                    lines.append("")
                    if image_path:
                        image_ref = rel_path(image_path, doc_path)
                        lines.append(f"{p}    ![{name} preview]({image_ref})")
                        lines.append("")
                    lines.append(f'{p}    [:material-github: `{page_path.name}`]({repo_blob_url(page_path)})')
                    lines.append("")
                lines.append(f"{p}</div>")
                lines.append("")
    else:
        lines.append("No layout metadata found.")
        lines.append("")

    lines.extend(render_tracking(tracking))

    return "\n".join(lines).rstrip() + "\n"


def parse_string_list(raw: Any) -> list[str]:
    if not isinstance(raw, list):
        return []
    return [str(item).strip() for item in raw if str(item).strip()]


def parse_tracking(meta: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(meta, dict):
        return {"state": "", "issues": [], "missing": [], "planned": []}
    return {
        "state": str(meta.get("state") or "").strip(),
        "issues": parse_string_list(meta.get("issues")),
        "missing": parse_string_list(meta.get("missing")),
        "planned": parse_string_list(meta.get("planned")),
    }


STATE_ADMONITION = {
    "stable": ("success", "Stable"),
    "active": ("info", "Active Development"),
    "wip": ("warning", "Work in Progress"),
}


def render_tracking(tracking: dict[str, Any]) -> list[str]:
    """Render tracking metadata as Material admonitions."""
    state = tracking.get("state", "")
    issues = tracking.get("issues", [])
    missing = tracking.get("missing", [])
    planned = tracking.get("planned", [])
    if not state and not issues and not missing and not planned:
        return []
    lines: list[str] = ["## Status", ""]
    if state:
        admonition_type, label = STATE_ADMONITION.get(state, ("note", state.title()))
        lines.extend([f'!!! {admonition_type} "State: {label}"', ""])
    if issues:
        lines.extend(['!!! bug "Known Issues"', ""])
        for item in issues:
            lines.append(f"    - {item}")
        lines.append("")
    if missing:
        lines.extend(['!!! warning "Missing"', ""])
        for item in missing:
            lines.append(f"    - {item}")
        lines.append("")
    if planned:
        lines.extend(['!!! tip "Planned"', ""])
        for item in planned:
            lines.append(f"    - {item}")
        lines.append("")
    return lines


def format_nav_yaml(aircraft_records: list[dict[str, Any]]) -> str:
    """Build the Decks nav section as YAML text (aircraft-only, no layout children)."""
    lines: list[str] = [
        "      - Overview: decks/index.md",
    ]
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
    MKDOCS_CONFIG.write_text(new_text, encoding="utf-8")


def build_index(aircraft_entries: list[dict[str, Any]]) -> str:
    lines = [
        "<!-- generated by scripts/generate_deck_docs.py; do not edit directly -->",
        "",
        "# Decks",
        "",
        '<div class="grid cards" markdown>',
        "",
    ]
    for entry in aircraft_entries:
        title = entry["title"]
        href = entry["href"]
        summary = entry["summary"]
        state = entry.get("state", "")
        tags = entry.get("tags", [])
        layout_count = entry.get("layout_count", 0)
        page_count = entry.get("page_count", 0)

        card: list[str] = []
        header = f"-   **{title}**"
        if state:
            header += f" · `{state}`"
        card.append(header)
        card.append("")
        card.append(f"    {summary}")
        card.append("")
        if tags:
            card.append(f"    {' · '.join(f'`{tag}`' for tag in tags)}")
            card.append("")
        details: list[str] = []
        if layout_count:
            details.append(f"{layout_count} layout{'s' if layout_count != 1 else ''}")
        if page_count:
            details.append(f"{page_count} page{'s' if page_count != 1 else ''}")
        if details:
            card.append(f"    {' · '.join(details)}")
            card.append("")
        card.append(f"    [:octicons-arrow-right-24: View deck]({href})")
        card.append("")
        lines.extend(card)

    lines.append("</div>")
    lines.append("")
    return "\n".join(lines)


def render_all_images(slug: str, config: dict[str, Any], deckconfig_dir: Path, docs_meta: dict[str, Any]) -> dict[str, dict[Path, Path]]:
    """Render preview images for all layouts; returns {layout_name: {page_path: image_path}}."""
    all_images: dict[str, dict[Path, Path]] = {}
    for layout in layout_entries(config, deckconfig_dir, docs_meta):
        if not layout["pages"]:
            continue
        images = render_layout_page_images(slug, layout)
        if not images:
            # Fall back to pre-existing images
            for page_path in layout["pages"]:
                image_path = page_image_path(slug, page_path)
                if image_path is None:
                    images = {}
                    break
                images[page_path] = image_path
        if images:
            all_images[layout["layout"]] = images
    return all_images


def main() -> int:
    DOCS_DECKS_DIR.mkdir(parents=True, exist_ok=True)

    aircraft_entries: list[dict[str, str]] = []
    aircraft_records: list[dict[str, Any]] = []
    for aircraft_dir in sorted(path for path in DECKS_DIR.iterdir() if path.is_dir()):
        deckconfig_dir = aircraft_dir / "deckconfig"
        config_path = deckconfig_dir / "config.yaml"
        if not config_path.exists():
            continue

        slug = aircraft_dir.name
        config = load_yaml(config_path)
        docs_meta = load_yaml(deckconfig_dir / "_docs.yaml") if (deckconfig_dir / "_docs.yaml").exists() else {}
        page_images = render_all_images(slug, config, deckconfig_dir, docs_meta)
        doc_path = DOCS_DECKS_DIR / slug / "index.md"
        doc_path.parent.mkdir(parents=True, exist_ok=True)
        doc_path.write_text(build_overview(slug, config, docs_meta, doc_path, page_images), encoding="utf-8")
        layouts = layout_entries(config, deckconfig_dir, docs_meta)

        aircraft_meta = normalize_docs_metadata(docs_meta.get("aircraft"))
        title = aircraft_title(slug, config, docs_meta)
        summary = str(aircraft_meta.get("summary") or config.get("description") or f"Deck definitions for {title}.")
        tracking = parse_tracking(docs_meta.get("tracking"))
        tags = aircraft_meta.get("tags", [])
        if not isinstance(tags, list):
            tags = []
        total_pages = sum(len(layout["pages"]) for layout in layouts)
        aircraft_entries.append(
            {
                "href": f"{slug}/index.md",
                "title": title,
                "summary": summary,
                "state": tracking.get("state", ""),
                "tags": tags,
                "layout_count": len(layouts),
                "page_count": total_pages,
            }
        )
        aircraft_records.append({"slug": slug, "title": title})

    (DOCS_DECKS_DIR / "index.md").write_text(build_index(aircraft_entries), encoding="utf-8")
    update_mkdocs_nav(aircraft_records)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
