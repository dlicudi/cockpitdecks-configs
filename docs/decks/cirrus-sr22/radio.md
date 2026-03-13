---
title: SR22 Radio
---

# SR22 Radio

## Overview { #sr22-radio-preview }

This page combines transponder-adjacent controls with COM, NAV, and ADF workflow.

- The top row is a compact squawk editor.
- The center of the page mixes transponder mode and `IDENT` with radio workflow.
- `COM 1`, `ADF`, and `VLOC 1` all show active and standby-style frequency information.

## What Is On The Page

| Control | Function |
| --- | --- |
| `SQUAWK0-3` | Increment each squawk digit directly |
| `TRANSPONDER` | Rotary-style transponder mode selector |
| `IDENT` | Send ident |
| `ADF FREQ` | Show active and standby ADF frequency and flip |
| `COM 1` | Show active and standby COM1 and flip |
| `VLOC 1` | Show active and standby NAV1 and flip |

## Encoders

| Encoder | Action |
| --- | --- |
| `e3` | Transponder paired-digit adjustment |
| `e4` | COM1 standby coarse/fine with flip on long press |
| `e5` | NAV1 standby coarse/fine with flip on long press |
| `e2` | ADF standby tuning with flip on long press |

## Side Screens

- Left screen: transponder code, transponder mode, and ADF standby.
- Right screen: COM standby and VLOC standby, plus an unused placeholder line.

!!! note
    This page intentionally overlaps with the dedicated transponder page. Use `radio` when you want COM/NAV/ADF and squawk changes together, and `transponder` when you want a full-page XPDR workflow.
