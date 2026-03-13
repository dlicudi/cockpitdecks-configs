---
title: SR22 Engine
---

# SR22 Engine

## Overview { #sr22-engine-preview }

Dedicated engine page for sustained power, fuel, temperature, and pressure monitoring.

- This page consolidates RPM, manifold pressure, temperatures, pressures, and fuel flow.
- Throttle and mixture get large segmented percentage readouts.
- The fuel selector is duplicated here so tank management stays available during engine monitoring.

## What Is On The Page

| Control | Function |
| --- | --- |
| `ENGINE_RPM` | Engine RPM |
| `MANIFOLD_PRESSURE` | Manifold pressure |
| `OIL_TEMP` | Oil temperature |
| `OIL_PRESSURE` | Oil pressure |
| `FUEL_FLOW` | Fuel flow |
| `CHT` | Cylinder head temperature |
| `BATTERY` | Battery watt-hours and amps |
| `THROTTLE` | Throttle percentage |
| `FUEL EST` | Estimated endurance |
| `FUEL_L` | Select left tank and show left quantity |
| `FUEL_R` | Select right tank and show right quantity |
| `MIXTURE` | Mixture percentage |

## Highlights

- This is the densest engine-monitoring page in the SR22 set.
- Throttle and mixture use large segmented percentage readouts.
- The fuel selector is duplicated here so you can manage tanks without leaving engine monitoring.

!!! note
    The engine page uses converted flow and endurance values rather than raw simulator units.

    Fuel flow is derived from the configured GPH conversion.
    ```text
    fuel_flow_kg_sec 3600 * 0.8 / 3.78541 / 2 roundn
    ```

    Fuel estimate is based on total fuel quantity divided by current flow.
    ```text
    total_fuel / fuel_flow_per_hour
    ```

## Encoders

The engine page inherits the FCU encoder set, so throttle, heading, baro, altitude, vertical speed, and mixture remain available while monitoring the engine.
