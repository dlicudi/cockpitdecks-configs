---
layout: default
title: Side Icon Examples
parent: Examples
has_children: false
nav_order: 6
---

# Side Icon Examples

## Left side display for SPD/HDG/QNH encoders

```
- index: left
  name: left_screen
  type: none
  side:
    icon-color: Black
    labels:
      - label: "SPD"
        label-size: 16
        label-font: B612-Bold
        label-color: Grey
        formula: "${data:sim/cockpit2/autopilot/airspeed_dial_kts_mach}"
        text-size: 16
        text-font: Seven Segment.ttf
        text-color: White
        text-format: "{0:00.0f}"
        text: "${formula}"
      - label: "HDG"
        label-size: 14
        label-font: B612-Bold
        label-color: Gold
        formula: "${sim/cockpit/autopilot/heading_mag}"
        text-size: 18
        text-font: Seven Segment.ttf
        text-color: White
        text-format: "{0:00.0f}"
        text: "${formula}"
      - label: "QNH"
        label-size: 14
        label-font: B612-Bold
        label-color: Gold
        formula: "${sim/cockpit2/gauges/actuators/barometer_setting_in_hg_pilot}"
        text-size: 18
        text-font: Seven Segment.ttf
        text-color: White
        text-format: "{0:01.2f}"
        text: "${formula}"
```

## Right side display for ALT/VS/MIX encoders


```
- index: right
  name: right_screen
  type: none
  side:
    icon-color: Black
    labels:
      - label: "ALT"
        label-size: 16
        label-font: B612-Bold
        label-color: Grey
        formula: "${sim/cockpit2/autopilot/altitude_dial_ft}"
        text-size: 16
        text-font: Seven Segment.ttf
        text-color: White
        text-format: "{0:04.0f}"
        text: "${formula}"
      - label: "VS"
        label-size: 14
        label-font: B612-Bold
        label-color: Gold
        formula: "${sim/cockpit/autopilot/vertical_velocity} 100 /"
        text-size: 18
        text-font: Seven Segment.ttf
        text-color: White
        text-format: "{0:+01.0f}"
        text: "${formula}"
      - label: "MIX"
        label-size: 14
        label-font: B612-Bold
        label-color: Gold
        formula: "${sim/flightmodel/engine/ENGN_mixt[0]} 100 *"
        text-size: 18
        text-font: Seven Segment.ttf
        text-color: White
        text-format: "{0:01.0f}"
        text: "${formula}%"
```