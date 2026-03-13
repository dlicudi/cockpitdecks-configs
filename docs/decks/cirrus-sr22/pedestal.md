---
title: SR22 Pedestal
---

# SR22 Pedestal

## Overview { #sr22-pedestal-preview }

The pedestal page groups together throttle, mixture, parking brake, and flap controls.

- `THROTTLE` and `MIXTURE` are shown as large percentage readouts.
- The middle controls cover parking brake and flap movement.
- This page uses a custom encoder map that leans more toward FMS/range and altitude workflow than the default FCU set.

## What Is On The Page

| Control | Function |
| --- | --- |
| `THROTTLE` | Throttle percentage |
| `MIXTURE` | Mixture percentage |
| `TOGGLE BRAKES` | Toggle parking brake and show ON/OFF |
| `UP` | Flaps up |
| `DOWN` | Flaps down |
| `FLAPS RATIO` | Numeric flap ratio with disagree indication |

## Encoders

The pedestal page uses its own encoder map:

- `e0`: range push/down/up
- `e1`: FMS outer+inner on turn, cursor on long press
- `e2`: BARO STD / down / up
- `e3`: altitude outer+inner, altitude sync on long press
- `e4`: vertical-speed sync / down / up
- `e5`: mixture max / down / up

## Side Screens

- Left screen: throttle, heading/FMS reference, and QNH.
- Right screen: selected altitude, vertical speed, and mixture.
