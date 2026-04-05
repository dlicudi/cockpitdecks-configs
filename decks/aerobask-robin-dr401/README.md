# Aerobask Robin DR401

Cockpitdecks configuration for the Aerobask Robin DR401.

## What Is In This Folder

- `deckconfig/config.yaml`: aircraft-level registration and defaults
- `deckconfig/loupedecklive1/`: Loupedeck Live layout
- `deckconfig/streamdeckxl1/`: Stream Deck XL layout
- `deckconfig/resources/`: local resources used by the config
- `deckconfig/secret.yaml.dist`: example local secret file

## Installation

Link this `deckconfig` folder into the matching aircraft folder in your X-Plane installation:

```sh
ln -s ~/GitHub/cockpitdecks-configs/decks/aerobask-robin-dr401/deckconfig \
  "<your X-Plane aircraft folder>/deckconfig"
```

If you need local secrets for your setup, start from:

```sh
cp deckconfig/secret.yaml.dist deckconfig/secret.yaml
```

## Layouts

Defined in `deckconfig/config.yaml`.

| Layout | Device | Pages |
|---|---|---:|
| `loupedecklive1` | Loupedeck Live | 13 |
| `streamdeckxl1` | Stream Deck XL | 12 |

## Pages

### Loupedeck Live

- `index`
- `pfi`
- `fcu`
- `g1000`
- `engine`
- `radio`
- `transponder`
- `weather`
- `pedestal`
- `views`
- `switches`
- `switches2`
- `audiopanel`

### Stream Deck XL

- `index`
- `pfd`
- `mfd`
- `fcu`
- `g1000`
- `engine`
- `radio`
- `transponder`
- `weather`
- `views`
- `switches`
- `audiopanel`

## Configuration State

This aircraft has both Loupedeck Live and Stream Deck XL layouts and looks reasonably complete at the page-structure level.

There is no manifest or explicit release metadata here, so this README does not claim a version or stability level beyond what is present in the folder.
