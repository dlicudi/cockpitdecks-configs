# Annunciator Buttons

## Displaying airspeed

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

## Displaying fuel tanks 
```
- index: 4 # Fuel
    name: FUEL
    type: none
    label: FUEL QTY
    label-color: Black
    label-size: 10
    annunciator:
      size: medium
      model: B
      parts:
        B0:
          color: yellow
          text-size: 32
          formula: "${sim/cockpit2/fuel/fuel_quantity[0]} 0.264172 * 2 roundn"
          text: "L ${formula} gal"
        B1:
          color: yellow
          text-size: 32
          formula: "${sim/cockpit2/fuel/fuel_quantity[1]} 0.264172 * 2 roundn"
          text: "R ${formula} gal"
```

## Displaying RPM and hobbs

```
  - index: 8
    name: RPM
    type: none
    label: RPM
    label-color: Black
    label-size: 10
    annunciator:
      size: medium
      model: B
      parts:
        B0:
          color: lime
          text-size: 42
          text: "${sim/cockpit2/engine/indicators/prop_speed_rpm[0]}"
          text-format: "{0:.0f}"
          formula: "1"
        B1:
          color: white
          text-size: 30
          text: "${sim/cockpit2/clock_timer/hobbs_time_hours}:${sim/cockpit2/clock_timer/hobbs_time_minutes}:${sim/cockpit2/clock_timer/hobbs_time_seconds}"
          formula: "1"
          text-format: "{0:.0f}"
```



## Caution Annunciator
```
  - index: 9
    name: CAUTION
    type: none
    label: CAUTION
    label-size: 10
    label-color: black
    annunciator:
      size: medium
      model: B
      parts:
        B0:
          text: "OIL PRESS"
          text-color: firebrick
          text-font: DIN Condensed Black.otf
          text-size: 50
          formula: ${sim/cockpit/warnings/annunciators/oil_pressure}
        B1:
          text: "VOLTS"
          text-color: firebrick
          text-font: DIN Condensed Black.otf
          text-size: 50
          formula: ${sim/cockpit/warnings/annunciators/generator}
```

``` py title="bubble_sort.py"
def bubble_sort(items):
    for i in range(len(items)):
        for j in range(len(items) - 1 - i):
            if items[j] > items[j + 1]:
                items[j], items[j + 1] = items[j + 1], items[j]
```

## Warning Annunciator

``` py title="Warning Annunciator"
  - index: 10
    name: WARNING
    type: none
    label: WARNING
    label-size: 10
    label-color: black
    annunciator:
      size: medium
      model: B
      parts:
        B0:
          text: "L FUEL R"
          text-color: darkorange
          text-font: DIN Condensed Black.otf
          text-size: 50
          formula: ${sim/cockpit/warnings/annunciators/fuel_pressure}
        B1:
          text: "L VAC R"
          text-color: darkorange
          text-font: DIN Condensed Black.otf
          text-size: 50
          formula: ${sim/cockpit/warnings/annunciators/low_vacuum}
```


## Test
Testing