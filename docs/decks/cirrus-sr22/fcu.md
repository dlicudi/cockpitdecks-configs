---
title: SR22 FCU
---

# SR22 FCU

## Overview { #sr22-fcu-preview }

The FCU page covers the SR22 autopilot and navigation-mode workflow.

- The top ten buttons are the core AP mode controls: `AP`, `FD`, `HDG`, `ALT`, `NAV`, `VNAV`, `APR`, `REV/BC`, `VS`, and `FLC`.
- The last two buttons switch HSI source between GPS and VOR inputs.
- Side screens keep selected heading, QNH, altitude, vertical speed, throttle, and mixture visible while you work the modes.

## Modes

| Control | Function |
| --- | --- |
| `AP` | Engage or disengage the autopilot. |
| `FD` | Enable the flight director cues without engaging full autopilot control. |
| `HDG` | Heading mode selection. |
| `ALT` | Altitude hold / altitude mode selection. |
| `NAV` | NAV tracking mode. |
| `VNAV` | Manage the aircraft's vertical path according to route or waypoint constraints. |
| `APR` | Approach mode. |
| `REV/BC` | Back-course / reverse sensing related mode. |
| `VS` | Vertical speed mode. |
| `FLC` | Maintain a selected airspeed while climbing or descending to a target altitude. |
| `HSI GPS` | Toggle HSI source between GPS 1 and GPS 2. |
| `HSI NAV` | Toggle HSI source between VOR 1 and VOR 2. |

## Layout Notes

- The annunciator buttons all use sharp `v` style with `light-off-intensity: 8`.
- The first ten buttons are mode buttons with a lit bar when active.
- The last two buttons are HSI source selectors rather than AP modes.
- `GPS` toggles between `GPS` and `GPS2`.
- `VOR` toggles between `VOR1` and `VOR2`.

## Encoders

| Encoder | Action |
| --- | --- |
| `e0` | Throttle full on push, throttle down/up on turn |
| `e1` | Heading sync on push, heading down/up on turn |
| `e2` | BARO STD on push, barometer down/up on turn |
| `e3` | G1000 altitude outer/inner on turn, altitude sync on long press |
| `e4` | Vertical-speed sync on push, VS down/up on turn |
| `e5` | Mixture max on push, mixture down/up on turn |

## Side Screens

- Left screen: throttle, current heading, and QNH.
- Right screen: selected altitude, vertical speed, and mixture.
- Both side screens have a render cooldown to reduce redraw churn during active page use.
