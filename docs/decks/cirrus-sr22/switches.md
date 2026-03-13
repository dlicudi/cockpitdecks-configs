---
title: SR22 Switches
---

# SR22 Switches

## Overview { #sr22-switches-preview }

This page concentrates the SR22 electrical, lighting, icing, and fuel-selector related controls.

- The top half covers ignition, avionics, batteries, and alternators.
- `LIGHTS` and `ICING` are dedicated subpages reached from this page.
- The bottom row exposes the SR22 fuel-selector states directly.

## Main Page

| Control | Function |
| --- | --- |
| `IGNITION` | Multi-position ignition plus starter hold |
| `AVIONICS` | Avionics master |
| `BAT 2` | Battery 2 |
| `BAT 1` | Battery 1 |
| `ALT 1` | Alternator 1 |
| `ALT 2` | Alternator 2 |
| `LIGHTS` | Jump to the dedicated lighting page |
| `ICING` | Jump to the dedicated anti-ice page |
| `FUEL OFF` | Left-off fuel selector state |
| `FUEL LEFT` | Left tank selected |
| `FUEL RIGHT` | Right tank selected |
| `FUEL OFF` | Right-off fuel selector state |

## Highlights

- `IGNITION` is the only multi-position starter control in the aircraft config.
- Electrical items are grouped on the top half of the page.
- Fuel-selector states occupy the bottom row so tank routing is visible at a glance.

## Lights

The linked `lights` page contains:

- `NAV`: wing and tail navigation lights
- `STROBE`: strobe lights
- `LAND`: landing light
- `ICE`: ice light for illuminating the leading edges

## Icing

The linked `icing` page contains:

- `PITOT`: pitot heat
- `ICE PROTECT`: de-icing fluid distribution
- `PUMP BKUP`: backup de-icing pump
- `NORM/HIGH`: icing system intensity selection
- `PROP`: propeller heat
- `WSHLD`: windshield de-icing

`NORM/HIGH` deserves special attention: `NORM` is intended for entering icing conditions, while `MAX` is for established ice accumulation and must be held for the duration of the process.

## Encoders

Like the home, PFI, and engine pages, `switches` inherits the FCU encoder set and side screens.
