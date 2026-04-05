# Embraer E-Jets Family

Cockpitdecks configuration for the Embraer E-Jets family.

The folder targets the E170/E175/E190/E195 cockpit family rather than a single tail-specific aircraft.

## What Is In This Folder

- `deckconfig/config.yaml`: aircraft-level registration
- `deckconfig/loupedecklive1/`: main Loupedeck Live layout
- `deckconfig/streamdeckxl1/`: Stream Deck XL layout
- `deckconfig/overhead/`: dedicated overhead layout
- `deckconfig/resources/`: local resources used by the config
- `deckconfig/secret.yaml.dist`: example local secret file

## Installation

Link this `deckconfig` folder into the matching aircraft folder in your X-Plane installation:

```sh
ln -s ~/GitHub/cockpitdecks-configs/decks/embraer-e-jets-family/deckconfig \
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
| `loupedecklive1` | Loupedeck Live | 28 |
| `streamdeckxl1` | Stream Deck XL | 14 |
| `overhead` | `e190.overhead.v2` | 1 |

## Pages

### Loupedeck Live

- `index`
- `pfi`
- `fcu`
- `fcu2`
- `g1000`
- `engine`
- `radio`
- `transponder`
- `weather`
- `views`
- `switches`
- `switches2`
- `audiopanel`
- `ground_services`
- `pedestal`
- `pedestal_powerplant`
- `overhead_apu_control`
- `overhead_cockpit_lights`
- `overhead_electric`
- `overhead_external_lights`
- `overhead_fire_extinguisher`
- `overhead_fuel`
- `overhead_hydraulic`
- `overhead_ice_protection`
- `overhead_passenger_signs`
- `overhead_pneumatic`
- `overhead_pressurization`
- `overhead_windshield_wiper`

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
- `switches2`
- `switches3`
- `audiopanel`
- `mfd`

### Overhead

- `index`

## Configuration State

This is a large config with broad page coverage, especially on the Loupedeck Live side.

It also looks uneven in places: the dedicated `overhead` layout is only a single page, and there is no manifest or explicit release/status metadata. Treat it as feature-rich, but not documented to the same standard as the Cirrus SR22 package.
