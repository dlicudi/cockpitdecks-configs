# Beechcraft Baron 58

Cockpitdecks configuration for the Beechcraft Baron 58.

## What Is In This Folder

- `deckconfig/config.yaml`: aircraft-level registration
- `deckconfig/loupedecklive1/`: Loupedeck Live layout
- `deckconfig/secret.yaml.dist`: example local secret file

## Installation

Link this `deckconfig` folder into the matching aircraft folder in your X-Plane installation:

```sh
ln -s ~/GitHub/cockpitdecks-configs/decks/beechcraft-baron-58/deckconfig \
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

## Pages

### Loupedeck Live

- `index`
- `pfi`
- `fcu`
- `g530`
- `engine`
- `radio`
- `transponder`
- `weather`
- `pedestal`
- `views`
- `switches`
- `switchesicing`
- `switcheslights`

## Configuration State

This config currently exposes a single Loupedeck Live layout.

That does not mean it is unusable, but it is narrower than the more complete dual-layout aircraft in this repository. The `config.yaml` also still contains `notes: TODO`, so the metadata is clearly not fully polished.
