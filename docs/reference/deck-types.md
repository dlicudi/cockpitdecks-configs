# Deck Types

Cockpitdecks deck type definitions describe the buttons, actions, and feedback available on each supported deck model.

The `.yaml` files that describe deck types belong in:

```text
cockpitdecks/decks/resources
```

## Actions

Supported interaction types include:

- `none`: display only
- `press`: single press event
- `longpress`: long-press event on decks that support it directly
- `push`: pressed and released events
- `encoder`: stepped rotary encoder input
- `cursor`: continuous slider/cursor input
- `swipe`: touch-surface gestures

In practice, `push` is the more flexible event type because it allows timing-sensitive actions such as long-press handling.

## Feedback

Supported feedback types include:

- `none`
- `led`
- `colored-led`
- `encoder-leds`
- `image`
- `vibrate`

## Deck Type YAML

Example:

```yaml
---
type: LoupedeckLive
driver: loupedeck
buttons:
  - name: 0
    action: push
    feedback: image
    image: [90, 90, 0, 0]
    repeat: 12
```

Key fields:

- `type`: the deck type name reported by the driver
- `driver`: the Cockpitdecks driver used for that hardware
- `action`: the supported interaction type for the control
- `feedback`: the supported output type for the control
- `image`: icon size and placement for screen-based controls
- `range`: min/max value range for sliders or cursor-style controls

## Drivers

Current driver families include:

- `streamdeck`
- `loupedeck`
- `xtouchmini`

For the original detailed notes, see [decktypes/README.md](../../decktypes/README.md) in the repository.
