#!/usr/bin/env python3
"""Regenerate deck overview docs from config."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any
import os
import re
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


def aircraft_index_doc_path(slug: str) -> Path:
    return DOCS_DECKS_DIR / slug / "index.md"


def rel_image_path(path: Path, doc_path: Path) -> str:
    return os.path.relpath(path, doc_path.parent).replace("\\", "/")


def built_page_asset_path(path: Path, doc_path: Path) -> str:
    return os.path.relpath(path, doc_path.parent).replace("\\", "/")


def rel_doc_link(target: Path, doc_path: Path) -> str:
    return os.path.relpath(target, doc_path.parent).replace("\\", "/")


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
    return str(aircraft_meta.get("title") or config.get("model") or config.get("aircraft") or titleize_slug(slug))


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


def build_layout_page(aircraft_title: str, title: str, layout: dict[str, Any], page_docs: list[dict[str, str]]) -> str:
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
    ]
    for page in page_docs:
        lines.extend(
            [
                f'## [{page["title"]}]({page["href"]})',
                "",
                f'![{page["title"]} preview]({page["image"]})',
                "",
            ]
        )
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
        f"![{title} preview]({image_ref})",
        "",
        "## Source",
        "",
        f'- [:material-github: `{page_path.parent.name}/{page_path.name}`]({repo_blob_url(page_path)})',
    ]

    if includes:
        include_links: list[str] = []
        for include in includes:
            include_path = page_path.parent / f"{include}.yaml"
            if include_path.exists():
                include_links.append(f'[:material-source-branch: `{include}.yaml`]({repo_blob_url(include_path)})')
            else:
                include_links.append(f"`{include}.yaml`")
        lines.extend(["", "- Includes: " + " · ".join(include_links)])

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
                    "href": f"{doc_stem}.md",
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
    ]
    if eyebrow:
        lines.extend([f"*{eyebrow}*", ""])
    lines.extend(
        [
            summary,
            "",
        ]
    )
    if tags:
        lines.extend([f"Tags: {' · '.join(f'`{tag}`' for tag in tags)}", ""])
    if hero_src:
        lines.extend([f"![{hero_alt}]({hero_src})", ""])
    lines.extend(["## Layouts", ""])

    if layouts:
        lines.extend(["| Layout | Summary |", "| --- | --- |"])
        for layout in layouts:
            layout_doc = ROOT / "docs" / "decks" / slug / layout["layout"] / "index.md"
            href = rel_doc_link(layout_doc, doc_path) if layout_doc.exists() else "#"
            page_count = len(layout["pages"])
            summary = f"`{layout['type']}` layout with {page_count} page{'s' if page_count != 1 else ''}."
            label = f"[{layout['title']}]({href})" if href != "#" else layout["title"]
            lines.append(f"| {label} | {summary} |")
    else:
        lines.append("- No layout metadata found.")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def normalize_tracking_metadata(meta: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(meta, dict):
        return {
            "state": "",
            "runtime_tested": None,
            "hardware_verified": None,
            "last_reviewed": "",
            "owner": "",
            "notes": "",
            "issues": [],
            "planned": [],
        }

    issues: list[dict[str, str]] = []
    raw_issues = meta.get("issues")
    if isinstance(raw_issues, list):
        for raw_issue in raw_issues:
            if not isinstance(raw_issue, dict):
                continue
            summary = str(raw_issue.get("summary") or "").strip()
            if not summary:
                continue
            issues.append(
                {
                    "summary": summary,
                    "severity": str(raw_issue.get("severity") or "minor").strip() or "minor",
                    "type": str(raw_issue.get("type") or "general").strip() or "general",
                    "status": str(raw_issue.get("status") or "open").strip() or "open",
                }
            )

    planned: list[str] = []
    raw_planned = meta.get("planned")
    if isinstance(raw_planned, list):
        for item in raw_planned:
            text = str(item).strip()
            if text:
                planned.append(text)

    return {
        "state": str(meta.get("state") or "").strip(),
        "runtime_tested": meta.get("runtime_tested") if isinstance(meta.get("runtime_tested"), bool) else None,
        "hardware_verified": meta.get("hardware_verified") if isinstance(meta.get("hardware_verified"), bool) else None,
        "last_reviewed": str(meta.get("last_reviewed") or "").strip(),
        "owner": str(meta.get("owner") or "").strip(),
        "notes": str(meta.get("notes") or "").strip(),
        "issues": issues,
        "planned": planned,
    }


def open_issues(tracking: dict[str, Any]) -> list[dict[str, str]]:
    return [issue for issue in tracking.get("issues", []) if issue.get("status") != "done"]


def planned_items(tracking: dict[str, Any]) -> list[str]:
    return tracking.get("planned", [])


def layout_doc_path(slug: str, layout_name: str) -> Path:
    return DOCS_DECKS_DIR / slug / layout_name / "index.md"


def layout_preview_dir(slug: str, layout_name: str) -> Path:
    return IMAGE_ROOT / slug / "generated" / layout_name


def layout_preview_count(slug: str, layout_name: str) -> int:
    preview_dir = layout_preview_dir(slug, layout_name)
    if not preview_dir.exists():
        return 0
    return len(list(preview_dir.glob("*.page.png")))


def nav_doc_paths() -> set[str]:
    if not MKDOCS_CONFIG.exists():
        return set()
    text = MKDOCS_CONFIG.read_text(encoding="utf-8")
    return set(re.findall(r"([A-Za-z0-9_./+-]+\.md)", text))


def layout_auto_findings(slug: str, layout: dict[str, Any]) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    docs_generated = layout_doc_path(slug, layout["layout"]).exists()
    preview_count = layout_preview_count(slug, layout["layout"])
    preview_mode = str(layout["docs"].get("preview") or "").strip().lower()
    decktype_path = layout.get("decktype_path")

    if not docs_generated:
        if preview_mode in {"none", "off", "static"}:
            findings.append(
                {
                    "severity": "minor",
                    "type": "docs",
                    "summary": "Layout docs are not generated because preview generation is disabled in metadata.",
                }
            )
        elif decktype_path is None:
            findings.append(
                {
                    "severity": "major",
                    "type": "metadata",
                    "summary": f"No decktype mapping found for `{layout['type']}`.",
                }
            )
        elif not has_supported_preview_geometry(decktype_path):
            findings.append(
                {
                    "severity": "major",
                    "type": "preview",
                    "summary": f"Preview renderer does not yet support `{layout['type']}`.",
                }
            )
        else:
            findings.append(
                {
                    "severity": "major",
                    "type": "docs",
                    "summary": "Layout docs were not generated.",
                }
            )

    if docs_generated and preview_count == 0:
        findings.append(
            {
                "severity": "major",
                "type": "preview",
                "summary": "Generated layout docs exist but preview assets are missing.",
            }
        )

    return findings


def build_status_page(aircraft_records: list[dict[str, Any]]) -> str:
    def status_aircraft_label(slug: str, title: str) -> str:
        compact = titleize_slug(slug)
        return compact if len(title) > 30 else title

    nav_paths = nav_doc_paths()
    auto_finding_rows: list[dict[str, str]] = []
    aircraft_rows: list[dict[str, str]] = []

    for record in aircraft_records:
        slug = record["slug"]
        title = record["title"]
        status_title = status_aircraft_label(slug, title)
        aircraft_tracking = normalize_tracking_metadata(record["docs_meta"].get("tracking"))
        layouts = record["layouts"]
        docs_generated_count = 0
        preview_generated_count = 0
        manual_issue_count = 0
        auto_finding_count = 0
        planned_count = 0

        manual_issues = open_issues(aircraft_tracking)
        planned = planned_items(aircraft_tracking)
        manual_issue_count += len(manual_issues)
        planned_count += len(planned)

        for layout in layouts:
            docs_generated = layout_doc_path(slug, layout["layout"]).exists()
            nav_exposed = f"decks/{slug}/{layout['layout']}/index.md" in nav_paths
            preview_count = layout_preview_count(slug, layout["layout"])
            auto_findings = layout_auto_findings(slug, layout)

            docs_generated_count += 1 if docs_generated else 0
            preview_generated_count += 1 if preview_count else 0
            auto_finding_count += len(auto_findings)

            for finding in auto_findings:
                auto_finding_rows.append(
                    {
                        "aircraft": status_title,
                        "aircraft_full": title,
                        "layout": layout["title"],
                        **finding,
                    }
                )

        aircraft_rows.append(
            {
                "aircraft": status_title,
                "aircraft_full": title,
                "state": aircraft_tracking.get("state") or "unknown",
                "runtime_tested": "yes" if aircraft_tracking.get("runtime_tested") is True else ("no" if aircraft_tracking.get("runtime_tested") is False else "unknown"),
                "hardware_verified": "yes" if aircraft_tracking.get("hardware_verified") is True else ("no" if aircraft_tracking.get("hardware_verified") is False else "unknown"),
                "manual_issues": str(manual_issue_count),
                "planned": str(planned_count),
                "auto_findings": str(auto_finding_count),
            }
        )

    lines = [
        "---",
        "title: Deck Status",
        "---",
        "",
        "<!-- generated by scripts/generate_deck_docs.py; do not edit directly -->",
        "",
        "# Deck Status",
        "",
        "Track declared deck state, known issues, planned work, and derived generation gaps from `deckconfig/_docs.yaml`.",
        "",
        "Metadata keys:",
        "- `tracking` for aircraft-level state",
        "- useful manual fields are `state`, `runtime_tested`, `hardware_verified`, `issues`, and `planned`",
        "",
        "## Summary",
        "",
        f"- Aircraft: {len(aircraft_rows)}",
        f"- Layouts: {sum(len(record['layouts']) for record in aircraft_records)}",
        "",
        "## Aircraft Matrix",
        "",
        "| Aircraft | State | Runtime Tested | Hardware Verified | Known Issues | Planned | Auto Findings |",
        "| --- | --- | --- | --- | ---: | ---: | ---: |",
    ]

    for row in aircraft_rows:
        lines.append(
            f"| {row['aircraft']} | `{row['state']}` | `{row['runtime_tested']}` | `{row['hardware_verified']}` | {row['manual_issues']} | {row['planned']} | {row['auto_findings']} |"
        )

    lines.append("")
    return "\n".join(lines)


def build_index(aircraft_entries: list[dict[str, str]]) -> str:
    lines = [
        "<!-- generated by scripts/generate_deck_docs.py; do not edit directly -->",
        "",
        "# Decks",
        "",
        "Browse the available config-driven deck docs.",
        "",
        "| Aircraft | Summary |",
        "| --- | --- |",
    ]
    for entry in aircraft_entries:
        lines.append(f'| [{entry["title"]}]({entry["href"]}) | {entry["summary"]} |')
    lines.append("")
    return "\n".join(lines)


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
        generate_layout_docs(slug, config, deckconfig_dir, docs_meta)
        doc_path = DOCS_DECKS_DIR / doc_filename(slug)
        overview = build_overview(slug, config, docs_meta, doc_path)
        doc_path.write_text(overview, encoding="utf-8")
        index_doc_path = aircraft_index_doc_path(slug)
        index_doc_path.parent.mkdir(parents=True, exist_ok=True)
        index_doc_path.write_text(build_overview(slug, config, docs_meta, index_doc_path), encoding="utf-8")
        layouts = layout_entries(config, deckconfig_dir, docs_meta)

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
                "href": f"{slug}/index.md",
                "image": image_ref,
                "title": title,
                "summary": summary,
            }
        )
        aircraft_records.append(
            {
                "slug": slug,
                "title": title,
                "config": config,
                "docs_meta": docs_meta,
                "layouts": layouts,
            }
        )

    (DOCS_DECKS_DIR / "index.md").write_text(build_index(aircraft_entries), encoding="utf-8")
    (DOCS_DECKS_DIR / "status.md").write_text(build_status_page(aircraft_records), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
