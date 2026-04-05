# Cessna 172 SP

Cockpitdecks configuration for the Laminar Research Cessna 172 SP.

## What Is In This Folder

- `deckconfig/config.yaml`: aircraft-level registration
- `deckconfig/loupedecklive1/`: Loupedeck Live layout
- `deckconfig/secret.yaml.dist`: example local secret file

## Installation

Link this `deckconfig` folder into the matching aircraft folder in your X-Plane installation:

```sh
ln -s ~/GitHub/cockpitdecks-configs/decks/cessna-172-sp/deckconfig \
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
| `loupedecklive1` | Loupedeck Live | 10 |

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
- `switches`

## Configuration State

This is a single-layout aircraft config aimed at the Loupedeck Live.

Compared with the Cirrus SR22 and some dual-layout aircraft, this package is smaller and more focused. There is no separate Stream Deck XL layout in this folder.
