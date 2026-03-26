#!/usr/bin/env python3
"""List, build, and release Cockpitdecks aircraft packs."""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
from pathlib import Path
from typing import Any
import zipfile

import yaml


ROOT = Path(__file__).resolve().parents[1]
DECKS_DIR = ROOT / "decks"
DIST_DIR = ROOT / "dist"
SKIP_NAMES = {".DS_Store", "_icon_cache.pickle"}


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a YAML mapping")
    return data


def resolve_pack_yaml(value: str) -> Path:
    candidate = Path(value)
    if candidate.suffix == ".yaml":
        if not candidate.is_absolute():
            candidate = (ROOT / candidate).resolve()
        return candidate
    return (DECKS_DIR / value / "pack.yaml").resolve()


def gh_quote(parts: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in parts)


def list_pack_yamls() -> list[Path]:
    return sorted(DECKS_DIR.glob("*/pack.yaml"))


def pack_data(pack_yaml: Path) -> dict[str, Any]:
    data = load_yaml(pack_yaml)
    pack_id = str(data.get("id") or "").strip()
    name = str(data.get("name") or pack_id).strip()
    version = str(data.get("version") or "").strip()
    if not pack_id:
        raise SystemExit(f"missing required 'id' in {pack_yaml}")
    if not version:
        raise SystemExit(f"missing required 'version' in {pack_yaml}")
    return {
        "yaml": pack_yaml,
        "dir": pack_yaml.parent,
        "id": pack_id,
        "name": name,
        "version": version,
        "tag": f"pack-{pack_id}-v{version}",
        "asset_name": f"{pack_id}-v{version}.zip",
        "asset_path": DIST_DIR / f"{pack_id}-v{version}.zip",
        "title": f"{name} Pack v{version}",
        "notes": f"Official {name} Cockpitdecks pack.",
        "meta": data,
    }


def included_files(pack_dir: Path) -> list[Path]:
    out: list[Path] = []
    for path in sorted(pack_dir.rglob("*")):
        if path.is_dir():
            continue
        if path.name in SKIP_NAMES:
            continue
        if path.name == "secret.yaml":
            continue
        out.append(path)
    return out


def build_pack(pack_yaml: Path) -> Path:
    info = pack_data(pack_yaml)
    pack_dir = info["dir"]
    asset_path = info["asset_path"]
    DIST_DIR.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(asset_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in included_files(pack_dir):
            arcname = Path(info["id"]) / path.relative_to(pack_dir)
            zf.write(path, arcname.as_posix())
    return asset_path


def gh_release_command(pack_yaml: Path) -> list[str]:
    info = pack_data(pack_yaml)
    return [
        "gh",
        "release",
        "create",
        info["tag"],
        str(info["asset_path"]),
        "--title",
        info["title"],
        "--notes",
        info["notes"],
    ]


def gh_release_state(pack_yaml: Path) -> dict[str, Any]:
    info = pack_data(pack_yaml)
    try:
        proc = subprocess.run(
            ["gh", "release", "view", info["tag"], "--json", "tagName,assets"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return {"gh_available": False, "release_exists": None, "asset_exists": None}
    except subprocess.CalledProcessError:
        return {"gh_available": True, "release_exists": False, "asset_exists": False}

    data = json.loads(proc.stdout)
    assets = data.get("assets") or []
    asset_names = {str(asset.get("name") or "").strip() for asset in assets if isinstance(asset, dict)}
    return {
        "gh_available": True,
        "release_exists": True,
        "asset_exists": info["asset_name"] in asset_names,
    }


def cmd_list(_: argparse.Namespace) -> int:
    for path in list_pack_yamls():
        info = pack_data(path)
        print(f"{info['id']}\tv{info['version']}\t{info['name']}")
    return 0


def cmd_info(args: argparse.Namespace) -> int:
    info = pack_data(resolve_pack_yaml(args.pack))
    state = gh_release_state(info["yaml"])
    print(f"pack_yaml: {info['yaml']}")
    print(f"id: {info['id']}")
    print(f"name: {info['name']}")
    print(f"version: {info['version']}")
    print(f"tag: {info['tag']}")
    print(f"asset: {info['asset_path']}")
    print(f"title: {info['title']}")
    print(f"gh: {gh_quote(gh_release_command(info['yaml']))}")
    print(f"gh_available: {state['gh_available']}")
    print(f"release_exists: {state['release_exists']}")
    print(f"asset_exists: {state['asset_exists']}")
    return 0


def cmd_build(args: argparse.Namespace) -> int:
    pack_yaml = resolve_pack_yaml(args.pack)
    asset_path = build_pack(pack_yaml)
    print(asset_path)
    return 0


def cmd_release(args: argparse.Namespace) -> int:
    pack_yaml = resolve_pack_yaml(args.pack)
    info = pack_data(pack_yaml)
    state = gh_release_state(pack_yaml)
    asset_path = build_pack(pack_yaml)
    command = gh_release_command(pack_yaml)
    print(f"asset: {asset_path}")
    print(f"gh: {gh_quote(command)}")
    print(f"release_exists: {state['release_exists']}")
    print(f"asset_exists: {state['asset_exists']}")
    if args.execute:
        if state["release_exists"] and state["asset_exists"]:
            raise SystemExit(f"release asset already exists for {info['tag']}: {info['asset_name']}")
        subprocess.run(command, check=True, cwd=ROOT)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="List, build, and release Cockpitdecks aircraft packs.")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="List known packs").set_defaults(func=cmd_list)

    info = sub.add_parser("info", help="Show derived release names and GitHub state for a pack")
    info.add_argument("pack", help="Pack id such as cirrus-sr22, or a path to pack.yaml")
    info.set_defaults(func=cmd_info)

    build = sub.add_parser("build", help="Build a pack zip into dist/")
    build.add_argument("pack", help="Pack id such as cirrus-sr22, or a path to pack.yaml")
    build.set_defaults(func=cmd_build)

    release = sub.add_parser("release", help="Build a pack zip and show or run gh release create")
    release.add_argument("pack", help="Pack id such as cirrus-sr22, or a path to pack.yaml")
    release.add_argument("--execute", action="store_true", help="Run the gh release create command")
    release.set_defaults(func=cmd_release)

    parser.add_argument("legacy_pack", nargs="?", help=argparse.SUPPRESS)
    args = parser.parse_args()

    if getattr(args, "legacy_pack", None) and args.command is None:
        args.command = "info"
        args.pack = args.legacy_pack
        args.func = cmd_info

    if not hasattr(args, "func"):
        return cmd_list(args)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
