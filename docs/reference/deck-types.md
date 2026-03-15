# Deck Types

Deck type definitions describe the buttons, actions, and feedback available on each supported deck model.
The `.yaml` files live in the [`decktypes/`](https://github.com/dlicudi/cockpitdecks-configs/tree/main/decktypes) directory.

## Supported Decks

### Physical

| Deck | Driver | Buttons | Notes |
|------|--------|---------|-------|
| Loupedeck Live | `loupedeck` | 12 image keys, 6 encoders, touchscreen strips | Primary development deck |
| Stream Deck XL | `streamdeck` | 32 image keys | Large grid layout |
| Stream Deck MK.2 | `streamdeck` | 15 image keys | Standard size |
| Stream Deck Mini | `streamdeck` | 6 image keys | Compact |
| Stream Deck Neo | `streamdeck` | 8 image keys + info strip | |
| Stream Deck + | `streamdeck` | 8 image keys + 4 encoders + touchscreen | |
| X-Touch Mini | `xtouchmini` | 16 buttons, 8 encoders, slider | MIDI controller |

### Virtual

Virtual decks mirror the layout of physical decks in a browser window — useful for
development and testing without hardware.

| Deck | Mirrors |
|------|---------|
| Virtual Loupedeck Live | Loupedeck Live |
| Virtual Streamdeck XL | Stream Deck XL |
| Virtual Streamdeck MK.2 | Stream Deck MK.2 |
| Virtual Streamdeck Mini | Stream Deck Mini |
| Virtual Streamdeck Neo | Stream Deck Neo |
| Virtual Streamdeck + | Stream Deck + |
| Virtual X-Touch Mini | X-Touch Mini |

## Actions

Supported interaction types:

| Action | Description |
|--------|-------------|
| `none` | Display only, no interaction |
| `press` | Single press event |
| `longpress` | Long-press event (decks that support it directly) |
| `push` | Pressed and released events — more flexible, allows timing-sensitive actions |
| `encoder` | Stepped rotary encoder input |
| `cursor` | Continuous slider/cursor input |
| `swipe` | Touch-surface gestures |

In practice, `push` is the more flexible event type because it allows timing-sensitive
actions such as long-press handling.

## Feedback

Supported output types:

| Feedback | Description |
|----------|-------------|
| `none` | No visual feedback |
| `led` | Single-colour LED |
| `colored-led` | RGB LED |
| `encoder-leds` | LED ring around encoder |
| `image` | Rendered image on key screen |
| `vibrate` | Haptic feedback |

## YAML Format

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

| Field | Description |
|-------|-------------|
| `type` | Deck type name reported by the driver |
| `driver` | Cockpitdecks driver for the hardware |
| `action` | Supported interaction type for the control |
| `feedback` | Supported output type for the control |
| `image` | Icon size and placement `[width, height, x, y]` for screen-based controls |
| `repeat` | Number of identical buttons in a grid |
| `range` | Min/max value range for sliders or cursor-style controls |

## Drivers

| Driver | Hardware |
|--------|----------|
| `streamdeck` | All Elgato Stream Deck models |
| `loupedeck` | Loupedeck Live and CT |
| `xtouchmini` | Behringer X-Touch Mini |

For the original detailed notes, see [`decktypes/README.md`](https://github.com/dlicudi/cockpitdecks-configs/blob/main/decktypes/README.md).
