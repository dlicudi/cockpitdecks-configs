---
layout: default
title: Examples
nav_order: 3
has_children: true
permalink: /docs/examples
---

# Examples


## Annunciator style button to display airspeed

```
  - index: 0
    name: SPD
    type: none
    label: SPD
    label-size: 9
    label-color: black
    annunciator:
      size: medium
      model: A
      parts:
        A0:
          color: lime
          text-size: 100
          formula: "1"
          text: "${sim/cockpit2/gauges/indicators/airspeed_kts_pilot}"
          text-font: Seven Segment.ttf
          text-format: "{0:.0f}"
```