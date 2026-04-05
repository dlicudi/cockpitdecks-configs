# cockpitdecks-configs

Aircraft deck configurations for [Cockpitdecks](https://github.com/dlicudi/cockpitdecks).

Repository-level docs live under `docs/`.
Aircraft-specific notes live in each aircraft `README.md`.

## Aircraft

| Pack | Aircraft | Available |
|------|----------|-----------|
| `cirrus-sr22` | Laminar Research Cirrus SR22 | Deck Packs tab |
| `cessna-172-sp` | Laminar Research Cessna 172 SP | Manual install |
| `beechcraft-baron-58` | Laminar Research Beechcraft Baron 58 | Manual install |
| `lancair-evolution` | Laminar Research Lancair Evolution | Manual install |
| `embraer-e-jets-family` | Laminar Research Embraer E-Jets Family | Manual install |
| `epic-e1000g` | Laminar Research Epic E1000G | Manual install |
| `vans-aircraft-rv-10` | Van's Aircraft RV-10 | Manual install |
| `aerobask-robin-dr401` | Aerobask Robin DR401 | Manual install |
| `toliss-airbus-a320-neo` | Toliss Airbus A320 Neo | Manual install |
| `toliss-airbus-a321-neo` | Toliss Airbus A321 Neo | Manual install |
| `toliss-airbus-a330-neo` | Toliss Airbus A330 Neo | Manual install |

## Installation

### Via Cockpitdecks Desktop (recommended)

Packs marked **Deck Packs tab** can be installed directly from the **Decks → Packs** tab in [Cockpitdecks Desktop](https://github.com/dlicudi/cockpitdecks-desktop). No manual steps required.

### Manual install

For configs without a published pack release, clone this repo and symlink the `deckconfig` folder into the aircraft directory:

```sh
git clone https://github.com/dlicudi/cockpitdecks-configs.git
```

Then symlink the config into your X-Plane aircraft folder:

```sh
ln -s ~/GitHub/cockpitdecks-configs/decks/cirrus-sr22/deckconfig \
  ~/X-Plane\ 12/Aircraft/Laminar\ Research/Cirrus\ SR22/deckconfig
```

> [!IMPORTANT]
> You must use a symlink — an alias (macOS Finder) will not work for long-press buttons.

### Installing Cockpitdecks

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install 'cockpitdecks[xplane,loupedeck] @ git+https://github.com/dlicudi/cockpitdecks.git'
```

`cockpitdecks-configs` is not a Python package and should not be installed with `pip`.

## Releasing a pack

```sh
# Preview
python scripts/release-deck.py release cirrus-sr22

# Publish
python scripts/release-deck.py release cirrus-sr22 --execute
```

Release notes are auto-generated from the git log since the previous tag. See each pack's `README.md` for aircraft-specific documentation.
