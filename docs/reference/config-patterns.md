# Config Patterns

Common YAML patterns used across aircraft configs.

This page is intentionally brief. It documents patterns that are actively used in this repository rather than preserving experimental implementation notes.

## Annunciators

Use `annunciator:` when a button is primarily a status display rather than an action target.

Typical uses in this repository:

- Audio panel source indicators
- Transponder digit and mode displays
- Warning and caution tiles
- Weather and engine status readouts

Example:

```yaml
- index: 8
  name: RPM
  type: none
  label: RPM
  label-color: black
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
        text: "${sim/cockpit2/clock_timer/hobbs_time_hours}:${sim/cockpit2/clock_timer/hobbs_time_minutes}"
        formula: "1"
```

Use live aircraft or module YAML as the source of truth when copying patterns:

- `modules/loupedecklive/audiopanel.yaml`
- `modules/streamdeckxl/transponder.yaml`
- aircraft-specific `includes/annunciators.yaml` files

## Side Displays

Use `side:` on Loupedeck side buttons when one control needs stacked labels and values.

Typical uses in this repository:

- FCU encoder readouts
- G1000 rotary selectors
- Radio and pedestal encoder status

Example:

```yaml
- index: left
  name: left_screen
  type: none
  side:
    icon-color: black
    labels:
      - label: SPD
        label-size: 16
        label-color: grey
        formula: "${sim/cockpit2/autopilot/airspeed_dial_kts_mach}"
        text-size: 16
        text-font: Seven Segment.ttf
        text-color: white
        text-format: "{0:00.0f}"
        text: "${formula}"
```

Reference live examples in:

- `decks/lancair-evolution/deckconfig/loupedecklive1/encoders/encoders_fcu.yaml`
- `decks/lancair-evolution/deckconfig/loupedecklive1/encoders/encoders_g1000.yaml`
- `decks/lancair-evolution/deckconfig/loupedecklive1/encoders/encoders_radio.yaml`

## Encoder Variants

Several aircraft use non-basic encoder types beyond a plain `encoder`.

### `encoder-toggle`

Used when push and rotate actions switch between two command sets, typically coarse vs. fine tuning or primary vs. secondary control.

Used in:

- `decks/epic-e1000g/deckconfig/loupedecklive1/encoders/`
- `decks/vans-aircraft-rv-10/deckconfig/loupedecklive1/encoders/`
- `decks/embraer-e-jets-family/deckconfig/loupedecklive1/encoders/`

### `encoder-value`

Used when the encoder writes a bounded numeric value directly, such as panel lighting or EFIS controls.

Used in:

- `decks/toliss-airbus-a330-neo/deckconfig/comm-radio/intlights.yaml`
- `decks/toliss-airbus-a330-neo/deckconfig/efis/index.yaml`
- `decks/toliss-airbus-a330-neo/deckconfig/comm-radio/encoders.yaml`

### `encoder-value-extended`

Used when a config needs larger steps, local cached values, or more advanced value handling than the basic variant.

Used in:

- `decks/embraer-e-jets-family/deckconfig/loupedecklive1/encoders/encoders_lights.yaml`
- `decks/vans-aircraft-rv-10/deckconfig/loupedecklive1/encoders/encoders_sound.yaml`

## Guidance

- Prefer copying from a working aircraft config instead of from old design notes.
- Keep docs focused on stable YAML patterns, not Python class internals.
- If a pattern is no longer used in the repository, it should usually not have a standalone docs page.
