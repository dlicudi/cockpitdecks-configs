# Cirrus SR22

Official Cockpitdecks configuration for the Laminar Research Cirrus SR22.

This is one of the most complete aircraft configs in this repository.

## Metadata

`manifest.yaml` declares:

- version: `1.1.2`
- status: `stable`
- summary: full G1000-focused SR22 coverage
- requires: `cockpitdecks`, `xplane`, `PI_CockpitdecksFMSBrowser`

## What Is In This Folder

- `deckconfig/config.yaml`: aircraft-level registration and tuning
- `manifest.yaml`: package metadata
- `deckconfig/loupedecklive1/`: main Loupedeck Live layout
- `deckconfig/streamdeckxl1/`: Stream Deck XL layout
- `deckconfig/webdeck1/`: minimal web deck
- `deckconfig/ipad1/`: iPad-oriented web deck
- `deckconfig/resources/`: local resources used by the config
- `deckconfig/secret.yaml.dist`: example local secret file

## Installation

Link this `deckconfig` folder into the Laminar SR22 folder:

```sh
ln -s ~/GitHub/cockpitdecks-configs/decks/cirrus-sr22/deckconfig \
  ~/X-Plane\ 12/Aircraft/Laminar\ Research/Cirrus\ SR22/deckconfig
```

If you need local secrets for your setup, start from:

```sh
cp deckconfig/secret.yaml.dist deckconfig/secret.yaml
```

## Requirements

- X-Plane 12 with the Laminar Research Cirrus SR22
- `cockpitdecks` with the X-Plane adapter
- matching deck support for your hardware
- `PI_CockpitdecksFMSBrowser` for the FMS pages

## Layouts

Defined in `deckconfig/config.yaml`.

| Layout | Device | Pages |
|---|---|---:|
| `loupedecklive1` | Loupedeck Live | 23 |
| `streamdeckxl1` | Stream Deck XL | 16 |
| `webdeck1` | Web deck | 1 |
| `ipad1` | SR22 iPad web deck | 10 |

Virtual Loupedeck Live, Virtual Stream Deck XL, and the `SR22 iPad` virtual web deck are also registered in `config.yaml`.

## Pages

### Loupedeck Live

- `index`
- `pfi`
- `fcu`
- `gcu479`
- `engine`
- `radio`
- `radio_com1`
- `radio_com2`
- `radio_nav1`
- `radio_nav2`
- `transponder`
- `weather`
- `views`
- `switches_master`
- `switches_ground`
- `switches_lights`
- `switches_icing`
- `fms_fpl`
- `fms_nav`
- `fms_load`
- `fms_proc_dep`
- `fms_proc_arr`
- `fms_proc_app`

### Stream Deck XL

- `index`
- `pfd`
- `mfd`
- `fcu`
- `gcu478`
- `engine`
- `radio`
- `transponder`
- `weather`
- `pedestal`
- `views`
- `switches`
- `icing`
- `lights`
- `fms`
- `fms_load`

### Web Deck

- `main`

### iPad Web Deck

- `main`
- `startup`
- `taxi`
- `approach`
- `pfd`
- `autopilot`
- `radio`
- `engine`
- `tuning`
- `systems`

## Configuration State

This is the best reference example in the repository for a fuller aircraft package.

It has the clearest metadata, multiple layouts, dedicated FMS pages, explicit requirements, and tuned dataref rounding in `config.yaml`. If another aircraft lacks documentation or structure, this is a reasonable model to follow.
