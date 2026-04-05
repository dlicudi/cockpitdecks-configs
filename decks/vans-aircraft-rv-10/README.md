# Van's Aircraft RV-10

Cockpitdecks configuration for the Van's Aircraft RV-10.

## What Is In This Folder

- `deckconfig/config.yaml`: aircraft-level registration and tuning
- `deckconfig/loupedecklive1/`: Loupedeck Live layout
- `deckconfig/streamdeckxl1/`: Stream Deck XL layout
- `deckconfig/resources/`: local resources used by the config
- `deckconfig/secret.yaml.dist`: example local secret file

## Installation

Link this `deckconfig` folder into the matching aircraft folder in your X-Plane installation:

```sh
ln -s ~/GitHub/cockpitdecks-configs/decks/vans-aircraft-rv-10/deckconfig \
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
| `streamdeckxl1` | Stream Deck XL | 13 |

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
- `pfi`
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
- `trutrak_sorcerer`

## Configuration State

This is a solid dual-layout aircraft config with both Loupedeck Live and Stream Deck XL coverage.

`config.yaml` also contains more careful dataref rounding and fetch-frequency tuning than many of the simpler aircraft folders, which suggests more operational refinement than the minimal single-layout packages.
