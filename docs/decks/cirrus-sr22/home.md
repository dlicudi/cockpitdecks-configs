---
title: SR22 Home
---

# SR22 Home

## Overview { #sr22-home-preview }

The home page is the entry point for the SR22 layout and provides quick access to the rest of the deck.

- Twelve main buttons jump straight into the working SR22 pages.
- `ICING` and `LIGHTS` are reachable from here even though they are not on the compact pager strip.
- The page keeps the FCU encoder set active, so heading, baro, altitude, and mixture remain available.

## What Is On The Page

| Button | Target |
| --- | --- |
| `PFI` | Primary flight and quick-reference page |
| `SWITCHES` | Electrical and fuel-selector page |
| `ICING` | Dedicated anti-ice page |
| `LIGHTS` | Dedicated lighting page |
| `FCU` | Autopilot and mode-control page |
| `GCU-478` | G1000 rotary/input page |
| `RADIO` | COM/NAV/ADF and partial transponder workflow |
| `ENGINE` | Full engine monitoring page |
| `PEDESTAL` | Throttle, mixture, brakes, flaps |
| `XPDR` | Dedicated transponder page |
| `WEATHER` | Weather utility page |
| `VIEWS` | Quick-look and camera page |

## Shared Navigation

Most SR22 pages also inherit the same hardware page shortcuts from `pager.yaml`:

- `b0`: Home
- `b1`: PFI
- `b2`: Switches
- `b3`: FCU
- `b4`: Radio
- `b5`: Engine
- `b6`: Pedestal
- `b7`: Transponder

## Encoders

The home page includes the FCU encoder set rather than a custom encoder map:

- left encoder pair: throttle, heading, baro
- right encoder pair: altitude, vertical speed, mixture
- side screens: throttle/heading/QNH on the left and altitude/VS/mixture on the right

## Notes

- This page is intended as the fastest route into the aircraft layout, not as an in-flight working page.
- `ICING` and `LIGHTS` are directly reachable here even though the compact pager buttons do not have dedicated shortcuts for them.
