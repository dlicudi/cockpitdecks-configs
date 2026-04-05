# ToLiss A321neo

Cockpitdecks configuration for the ToLiss A321neo cockpit family.

`deckconfig/config.yaml` explicitly says this folder is intended for the ToLiss A321 plus neo add-on, and notes that the same cockpit family is shared across variants.

## What Is In This Folder

- `deckconfig/config.yaml`: aircraft-level registration and styling
- `deckconfig/fcu/`: Loupedeck Live FCU-focused layout
- `deckconfig/efis-ecam/`: Stream Deck Original layout
- `deckconfig/panels/`: Stream Deck XL layout
- `deckconfig/efis/`: Stream Deck + layout
- `deckconfig/comm-radio/`: X-Touch Mini layout

## Installation

Link this `deckconfig` folder into the matching aircraft folder in your X-Plane installation:

```sh
ln -s ~/GitHub/cockpitdecks-configs/decks/toliss-airbus-a321-neo/deckconfig \
  "<your X-Plane aircraft folder>/deckconfig"
```

Adjust the target path to your local ToLiss A321/A321neo installation.

## Layouts

Defined in `deckconfig/config.yaml`.

| Layout | Device | Pages |
|---|---|---:|
| `fcu` | Loupedeck Live | 6 |
| `efis-ecam` | Stream Deck Original | 2 |
| `panels` | Stream Deck XL | 21 |
| `efis` | Stream Deck + | 1 |
| `comm-radio` | X-Touch Mini | 4 |

## Pages

### `fcu` layout

- `index`
- `fcu`
- `toliss`
- `popups`
- `views`
- `xpndr`

### `efis-ecam` layout

- `index`
- `efis`

### `panels` layout

- `index`
- `index-alt`
- `dashboard`
- `efis`
- `ecam`
- `radio`
- `xpndr`
- `aptnav`
- `adirs`
- `doors`
- `intlights`
- `piedestal`
- `popups`
- `toliss`
- `xplane`
- `cockpitdecks`
- `ovrhdaircond`
- `ovrhdelec`
- `ovrhdfire`
- `ovrhdfuel`
- `ovrhdhyd`

### `efis` layout

- `index`

### `comm-radio` layout

- `a`
- `b`
- `encoders`
- `intlights`

## Configuration State

This is a broad multi-device Airbus config with specialized layouts rather than one uniform page set across devices.

It looks substantial, especially on the Stream Deck XL side, but it is also clearly tailored to one maintainer's workflow. This README does not claim wider completeness than what the current page files show.
