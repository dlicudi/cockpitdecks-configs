#!/usr/bin/env python3
"""
X-Plane Web API helper: activate a command or get/set a dataref by simulator path.

Examples:
  xp_webapi.py cockpitdecks/fms_legs/scroll_down
  xp_webapi.py cockpitdecks/fms_legs/page
  xp_webapi.py cockpitdecks/fms_legs/window_start 2
  xp_webapi.py cockpitdecks/fms_browser/list_scroll_down

Requires X-Plane running with Web API enabled (default http://127.0.0.1:8086, v3).
"""
from __future__ import annotations

import argparse
import base64
import json
import sys
import urllib.error
import urllib.parse
import urllib.request


def _request(
    method: str,
    url: str,
    *,
    data: dict | None = None,
    headers: dict | None = None,
) -> tuple[int, object]:
    h = {"Accept": "application/json"}
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        h["Content-Type"] = "application/json"
    else:
        body = None
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=body, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            code = resp.status
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        code = e.code
        return code, raw
    if not raw:
        return code, None
    try:
        return code, json.loads(raw)
    except json.JSONDecodeError:
        return code, raw


def _filter_url(base: str, kind: str, name: str) -> str:
    q = urllib.parse.urlencode([("filter[name]", name)])
    return f"{base}/{kind}?{q}"


def _first_id(payload: object) -> int | None:
    if not isinstance(payload, dict):
        return None
    data = payload.get("data")
    if not data or not isinstance(data, list) or not data:
        return None
    first = data[0]
    if isinstance(first, dict) and "id" in first:
        return int(first["id"])
    return None


def _meta_first(payload: object) -> dict | None:
    if not isinstance(payload, dict):
        return None
    data = payload.get("data")
    if not data or not isinstance(data, list) or not data:
        return None
    if isinstance(data[0], dict):
        return data[0]
    return None


def _format_value(data: object) -> str:
    """Pretty-print a /datarefs/{id}/value \"data\" field."""
    if data is None:
        return "null"
    if isinstance(data, (int, float, bool)):
        return json.dumps(data)
    if isinstance(data, str):
        try:
            dec = base64.b64decode(data, validate=True).decode("utf-8")
        except (ValueError, UnicodeDecodeError):
            return json.dumps(data)
        if dec.startswith("{") or dec.startswith("["):
            try:
                return json.dumps(json.loads(dec), indent=2)
            except json.JSONDecodeError:
                pass
        return dec
    return repr(data)


def _parse_patch_value(s: str) -> str | int | float | bool:
    sl = s.lower()
    if sl == "true":
        return True
    if sl == "false":
        return False
    try:
        return int(s, 10)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        pass
    return s


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Run X-Plane Web API command or get/set dataref by path.",
    )
    ap.add_argument("--host", default="127.0.0.1", help="Web API host")
    ap.add_argument("--port", type=int, default=8086, help="Web API port")
    ap.add_argument("--version", default="v3", help="API version path segment (default v3)")
    ap.add_argument(
        "--duration",
        type=float,
        default=0.0,
        help="Command activate duration in seconds (default 0 = fire-and-release)",
    )
    ap.add_argument(
        "path",
        help="Command or dataref path (e.g. cockpitdecks/fms_legs/scroll_down)",
    )
    ap.add_argument(
        "value",
        nargs="?",
        help="If set: PATCH this dataref to the value (writable datarefs only). "
        "Parses int/float/bool or uses string.",
    )
    args = ap.parse_args()
    base = f"http://{args.host}:{args.port}/api/{args.version}"
    path = args.path

    if args.value is not None:
        url = _filter_url(base, "datarefs", path)
        code, payload = _request("GET", url)
        if code != 200:
            print(f"GET dataref filter failed HTTP {code}: {payload}", file=sys.stderr)
            return 1
        meta = _meta_first(payload)
        if not meta:
            print(f"No dataref named {path!r}", file=sys.stderr)
            return 1
        if not meta.get("is_writable"):
            print(f"Dataref {path!r} is not writable", file=sys.stderr)
            return 1
        ident = int(meta["id"])
        val = _parse_patch_value(args.value)
        purl = f"{base}/datarefs/{ident}/value"
        pcode, pbody = _request("PATCH", purl, data={"data": val})
        if pcode != 200:
            print(f"PATCH failed HTTP {pcode}: {pbody}", file=sys.stderr)
            return 1
        print(f"PATCH {path} (id={ident}) data={val!r} -> HTTP {pcode}")
        return 0

    # No value: try command first, then dataref get
    curl = _filter_url(base, "commands", path)
    code, payload = _request("GET", curl)
    cmd_id = _first_id(payload) if code == 200 else None

    if cmd_id is not None:
        aurl = f"{base}/command/{cmd_id}/activate"
        acode, abody = _request("POST", aurl, data={"duration": args.duration})
        if acode != 200:
            print(f"POST activate failed HTTP {acode}: {abody}", file=sys.stderr)
            return 1
        print(f"command {path} (id={cmd_id}) activate duration={args.duration} -> HTTP {acode}")
        return 0

    durl = _filter_url(base, "datarefs", path)
    dcode, dpayload = _request("GET", durl)
    if dcode != 200:
        print(f"GET dataref filter failed HTTP {dcode}: {dpayload}", file=sys.stderr)
        return 1
    dref_id = _first_id(dpayload)
    if dref_id is None:
        print(
            f"Unknown path {path!r}: not a command and not a dataref (check plugin loaded / spelling).",
            file=sys.stderr,
        )
        return 1

    vurl = f"{base}/datarefs/{dref_id}/value"
    vcode, vpayload = _request("GET", vurl)
    if vcode != 200:
        print(f"GET value failed HTTP {vcode}: {vpayload}", file=sys.stderr)
        return 1
    if isinstance(vpayload, dict) and "data" in vpayload:
        print(f"dataref {path} (id={dref_id}) value:")
        print(_format_value(vpayload["data"]))
    else:
        print(vpayload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
