---
layout: default
title: Engine
parent: Cessna 172 SP
grand_parent: Decks
has_children: false
nav_order: 5
---

Page
{: .label .float-right}

# Engine
![](../../../assets/images/engine.png)

## ENG RPM
Displays engine/prop RPM.

## MANIFOLD PRESSURE
Displays manifold pressure.

## OIL TEMP
Displays oil temperature.

## OIL PRESSURE
Displays oil pressure.

## FUEL FLOW
Display fuel flow in GPH.

```fuel_flow_kg_sec 3600 * 0.8 / 3.78541 / 2 roundn```

## CHT
Displays cylinder head temp in celsius.

## BATTERY
1. Displays battery charge in watts per hour.
2. Displays battery amps (negative value means battery is discharging)

## THROTTLE
Displays throttle as a percentage.

## FUEL EST
Provides an estimate on fuel remaining in hours, based on current fuel flow.

```fuel_flow_kg_sec[0]} 3 roundn 0.000001 + / 3600 / 1 roundn```

## MIXTURE
Displays fuel mixture as a percentage.