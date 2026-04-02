# Cirrus SR22

Official Cockpitdecks configuration for the Laminar Research Cirrus SR22.

Release metadata (version, status, dependencies) is in `manifest.yaml`.

## Requirements

- X-Plane 12 with the Laminar Research Cirrus SR22
- `cockpitdecks` with the X-Plane adapter (`cockpitdecks_xp`)
- Hardware driver matching your device:
  - `cockpitdecks_ld` — Loupedeck Live
  - `cockpitdecks_sd` — Stream Deck XL
- `PI_CockpitdecksFMSBrowser` X-Plane plugin for FMS pages (FPL / NAV / Load)

## Install

Clone or copy this config so the aircraft folder contains a `deckconfig` directory.

```sh
ln -s ~/GitHub/cockpitdecks-configs/decks/cirrus-sr22/deckconfig \
  ~/X-Plane\ 12/Aircraft/Laminar\ Research/Cirrus\ SR22/deckconfig
```

If you use a Loupedeck device, copy `secret.yaml.dist` to `secret.yaml` and set the device serial number:

```sh
cp deckconfig/secret.yaml.dist deckconfig/secret.yaml
```

## Layouts

Defined in `deckconfig/config.yaml`. Three layouts are included:

| Layout | Device | Status |
|--------|--------|--------|
| `loupedecklive1` | Loupedeck Live | Full |
| `streamdeckxl1` | Stream Deck XL | Full |
| `webdeck1` | Virtual / Web deck | Minimal |

Virtual equivalents of the Loupedeck and Stream Deck XL layouts are also available for testing without hardware.

## Pages

### Loupedeck Live (`loupedecklive1`)

| Page | Description |
|------|-------------|
| `index` / `index2` | Home |
| `pfi` | Primary Flight Instruments |
| `fcu` | Flight Control Unit (autopilot) |
| `gcu479` | GCU 479 keypad |
| `engine` | Engine monitoring |
| `radio` | Radio overview + COM1/2, NAV1/2 sub-pages |
| `transponder` | Transponder |
| `weather` | Weather |
| `pedestal` | Pedestal controls |
| `views` | View control |
| `switches_master` / `switches_ground` / `switches_lights` / `switches_icing` | Switch groups |
| `fms_fpl` | FMS — Flight Plan |
| `fms_nav` | FMS — Navigation |
| `fms_load` | FMS — Load flight plan |

### Stream Deck XL (`streamdeckxl1`)

| Page | Description |
|------|-------------|
| `index` | Home |
| `pfd` | Primary Flight Display |
| `fcu` | Flight Control Unit (autopilot) |
| `gcu478` | GCU 478 keypad |
| `mfd` | Multi-Function Display |
| `engine` | Engine monitoring |
| `radio` | Radios |
| `transponder` | Transponder |
| `weather` | Weather |
| `pedestal` | Pedestal controls |
| `views` | View control |
| `switches` | Switches |
| `icing` | Ice protection |
| `lights` | Lighting |
| `fms` | FMS — Flight Plan |
| `fms_load` | FMS — Load flight plan |
