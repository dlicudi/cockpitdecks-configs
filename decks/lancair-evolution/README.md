# Lancair Evolution

Cockpitdecks configuration for the Lancair Evolution.

## What Is In This Folder

- `deckconfig/config.yaml`: aircraft-level registration
- `deckconfig/loupedecklive1/`: Loupedeck Live layout
- `deckconfig/streamdeckxl1/`: Stream Deck XL layout
- `deckconfig/secret.yaml.dist`: example local secret file

## Installation

Link this `deckconfig` folder into the matching aircraft folder in your X-Plane installation:

```sh
ln -s ~/GitHub/cockpitdecks-configs/decks/lancair-evolution/deckconfig \
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
| `streamdeckxl1` | Stream Deck XL | 11 |

## Pages

### Loupedeck Live

- `home`
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
- `pfi`
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

This looks like a reasonably complete dual-layout aircraft config.

There is no explicit manifest or declared stability metadata, so this README only claims what is visible in the folder structure and page files.
