# Epic E1000G

Cockpitdecks configuration for the Aerobask Epic E1000G.

## What Is In This Folder

- `deckconfig/config.yaml`: aircraft-level registration
- `deckconfig/loupedecklive1/`: main Loupedeck Live layout
- `deckconfig/streamdeckxl1/`: partial Stream Deck XL layout
- `deckconfig/secret.yaml.dist`: example local secret file

## Installation

Link this `deckconfig` folder into the matching aircraft folder in your X-Plane installation:

```sh
ln -s ~/GitHub/cockpitdecks-configs/decks/epic-e1000g/deckconfig \
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
| `loupedecklive1` | Loupedeck Live | 17 |
| `streamdeckxl1` | Stream Deck XL | 2 |

## Pages

### Loupedeck Live

- `home`
- `pfd`
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
- `switches_ice`
- `switches_lights`
- `switches_prestart`
- `switches_pretaxi`
- `switches_systems`

### Stream Deck XL

- `switches`
- `switches2`

## Configuration State

This aircraft has a substantial Loupedeck Live layout, but the Stream Deck XL side is clearly incomplete.

That is not guesswork: the `streamdeckxl1` folder currently contains only two non-config pages. If you use the Loupedeck Live, this folder looks much stronger than if you use the Stream Deck XL.
