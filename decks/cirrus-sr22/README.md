# Cirrus SR22

Official Cockpitdecks configuration for the Laminar Research Cirrus SR22.

Release metadata for this pack is stored in `pack.yaml`.

## Status

- Aircraft: Laminar Research Cirrus SR22
- ICAO: `SR22`
- Config root: `deckconfig/`
- Included layouts:
  - `loupedecklive1`
  - `streamdeckxl1`

The Loupedeck Live layout is currently the most complete documented layout.

## Requirements

- X-Plane 12 with the Laminar Research Cirrus SR22
- `cockpitdecks`
- Matching Cockpitdecks runtime dependencies for your hardware
- One of:
  - Loupedeck Live
  - Stream Deck XL

Optional:

- `PI_CockpitdecksFMSBrowser` for FMS Load / FPL / NAV pages on the Loupedeck Live layout

## Install

Clone or copy this aircraft config so that the aircraft can see its `deckconfig` folder.

Example:

```sh
ln -s ~/GitHub/cockpitdecks-configs/decks/cirrus-sr22/deckconfig \
  ~/X-Plane\ 12/Aircraft/Laminar\ Research/Cirrus\ SR22/deckconfig
```

If you use a Loupedeck device, copy `secret.yaml.dist` to `secret.yaml` and set the device serial number:

```sh
cp deckconfig/secret.yaml.dist deckconfig/secret.yaml
```

## Notes

- `deckconfig/config.yaml` defines both included layouts.
- The FMS-related Loupedeck pages require the Cockpitdecks FMS browser plugin in X-Plane.
- The config includes local icons and fonts under `deckconfig/resources/`.

## Pages

Main pages currently included across the layouts:

- Home / index
- PFI
- FCU
- GCU478
- Engine
- Radio
- Transponder
- Weather
- Lights
- Icing
- Pedestal
- Views
- FMS-related pages

## Screenshots

### Cockpit

![Cockpit](../../docs/assets/images/cirrus-sr22/cirrus-sr22-cockpit.png)

### Home

![Home](../../docs/assets/images/cirrus-sr22/home.png)

### PFI

![PFI](../../docs/assets/images/cirrus-sr22/pfi.png)

### GCU478

![GCU478](../../docs/assets/images/cirrus-sr22/gcu478.png)

## Changelog

## [1.0.0] - 2024-06-11

- Added: New changelog
