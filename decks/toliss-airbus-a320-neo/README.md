# ToLiss Airbus A320neo

Cockpitdecks configuration for the ToLiss Airbus A320neo.

## What Is In This Folder

- `deckconfig/config.yaml`: aircraft-level registration
- `deckconfig/loupedecklive1/`: Loupedeck Live layout
- `deckconfig/streamdeckxl1/`: Stream Deck XL layout
- `deckconfig/overhead/`: overhead folder present, but no standalone page YAML beyond configuration

## Installation

Link this `deckconfig` folder into the matching aircraft folder in your X-Plane installation:

```sh
ln -s ~/GitHub/cockpitdecks-configs/decks/toliss-airbus-a320-neo/deckconfig \
  "<your X-Plane aircraft folder>/deckconfig"
```

Adjust the target path to your local ToLiss A320neo installation.

## Layouts

Defined in `deckconfig/config.yaml`.

| Layout | Device | Pages |
|---|---|---:|
| `loupedecklive1` | Loupedeck Live | 7 |
| `streamdeckxl1` | Stream Deck XL | 14 |
| `overhead` | folder present | 0 |

## Pages

### Loupedeck Live

- `index`
- `pfi`
- `fcu`
- `radio`
- `transponder`
- `views`
- `weather`

### Stream Deck XL

- `home`
- `pfi`
- `fcu`
- `g1000`
- `engine`
- `radio`
- `transponder`
- `weather`
- `views`
- `pedestal`
- `audiopanel`
- `switches`
- `switches2`
- `overhead_antiice`

## Configuration State

This config is uneven.

The Stream Deck XL layout is much broader than the Loupedeck Live layout, and the `overhead/` directory currently contains only `config.yaml`, not a usable page set. This README therefore treats the aircraft as present and usable, but not as complete as the stronger packages in the repository.
