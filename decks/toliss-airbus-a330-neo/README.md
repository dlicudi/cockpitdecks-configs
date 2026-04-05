# ToLiss A330neo

Cockpitdecks configuration for the ToLiss A330neo.

This folder includes both physical and virtual deck registrations.

## What Is In This Folder

- `deckconfig/config.yaml`: aircraft-level registration and styling
- `deckconfig/fcu/`: Loupedeck Live layout
- `deckconfig/efis-ecam/`: Stream Deck Original layout
- `deckconfig/panels/`: Stream Deck XL layout
- `deckconfig/efis/`: Stream Deck + layout
- `deckconfig/comm-radio/`: X-Touch Mini layout
- `deckconfig/vmini/`: Virtual Stream Deck Mini layout
- `deckconfig/vneo/`: Virtual Stream Deck Neo layout

## Installation

Link this `deckconfig` folder into the matching aircraft folder in your X-Plane installation:

```sh
ln -s ~/GitHub/cockpitdecks-configs/decks/toliss-airbus-a330-neo/deckconfig \
  "<your X-Plane aircraft folder>/deckconfig"
```

Adjust the target path to your local ToLiss A330neo installation.

## Layouts

Defined in `deckconfig/config.yaml`.

| Layout | Device | Pages |
|---|---|---:|
| `fcu` | Loupedeck Live | 5 |
| `efis-ecam` | Stream Deck Original | 2 |
| `panels` | Stream Deck XL | 21 |
| `efis` | Stream Deck + | 1 |
| `comm-radio` | X-Touch Mini | 4 |
| `vmini` | Virtual Stream Deck Mini | 1 |
| `vneo` | Virtual Stream Deck Neo | 1 |

`config.yaml` also registers several virtual deck variants that reuse existing layouts, including virtual Stream Deck XL, Stream Deck +, Loupedeck Live, and X-Touch Mini.

## Pages

### `fcu` layout

- `index`
- `fcu`
- `toliss`
- `popups`
- `views`

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

### Virtual-only layouts

- `vmini/index`
- `vneo/index`

## Configuration State

This is a large and flexible Airbus config with the widest explicit virtual-deck registration in the repository.

At the same time, the existing `config.yaml` comments describe it as a development-oriented configuration that may still need adjustment for production use. This README keeps that caveat because it is stated directly in the source folder.
