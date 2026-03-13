---
title: SR22 PFI
---

# SR22 PFI

## Overview { #sr22-pfi-preview }

The PFI page combines primary flight information with a few engine-adjacent and navigation-adjacent quick-reference items.

- Primary scan items are `SPD`, `HDG`, `ALT`, and `VS`.
- Engine-adjacent references include fuel quantity, EGT/fuel flow, oil, vacuum/amps, and RPM/Hobbs.
- `CAUTION`, `WARNING`, and `NEXT WAYPOINT` make this the best quick-reference page while flying.

## What Is On The Page

| Position | Function |
| --- | --- |
| `SPD` | Airspeed in knots |
| `HDG` | Magnetic heading |
| `ALT` | Altitude with baro in inHg and hPa |
| `VS` | Vertical speed |
| `FUEL QTY` | Left and right fuel quantity in gallons |
| `EGT/FF` | EGT and fuel flow |
| `OIL` | Oil temperature and pressure |
| `VAC/AMP` | Vacuum and battery amps |
| `RPM` | Propeller RPM and Hobbs time |
| `CAUTION` | Oil pressure and volts cautions |
| `WARNING` | Fuel pressure and low-vac warnings |
| `NEXT WAYPOINT` | Waypoint ID, distance, DTK, ETA |

## Highlights

- The four primary instruments use segmented-style readouts for quick scanning.
- `CAUTION` and `WARNING` now use sharp `v` annunciators with dim off-state instead of Korry blur.
- `NEXT WAYPOINT` uses a four-field waypoint card with waypoint ID, distance, track, and ETA.

## Encoders And Side Screens

The page inherits the FCU encoder set:

- `e0`: throttle full / down / up
- `e1`: heading sync / heading down / heading up
- `e2`: baro STD / baro down / baro up
- `e3`: G1000 altitude outer+inner plus altitude sync on long press
- `e4`: vertical-speed sync / down / up
- `e5`: mixture max / down / up

The left side screen shows throttle, heading, and QNH. The right side screen shows selected altitude, vertical speed, and mixture.

## Notes

- Fuel quantity is converted to gallons with `0.264172 *`.
- The fuel-flow field uses a custom GPH formula based on `sim/flightmodel/engine/ENGN_FF_[0]`.
- This page is for quick-reference flying, not as a complete PFD replacement.
