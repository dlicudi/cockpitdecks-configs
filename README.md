# cockpitdecks-configs

Aircraft deck configurations for [Cockpitdecks](https://github.com/dlicudi/cockpitdecks).

Repository-level docs live under `docs/`. Aircraft-specific notes live in each aircraft `README.md`.

## Aircraft

Aircraft configs currently live under `decks/`.

`cirrus-sr22` is available from the Cockpitdecks Desktop pack browser. The rest are manual install configs for now.

## Installation

### Desktop

Install published packs from **Decks → Packs** in [Cockpitdecks Desktop](https://github.com/dlicudi/cockpitdecks-desktop).

### Manual install

Clone the repo:

```sh
git clone https://github.com/dlicudi/cockpitdecks-configs.git
```

Link the aircraft `deckconfig` into the matching X-Plane aircraft folder:

```sh
ln -s ~/GitHub/cockpitdecks-configs/decks/cirrus-sr22/deckconfig \
  ~/X-Plane\ 12/Aircraft/Laminar\ Research/Cirrus\ SR22/deckconfig
```

Use a real symlink created with `ln -s`, not a Finder alias. Finder aliases are macOS shortcuts and can break Cockpitdecks behavior, including long-press handling.

### Installing Cockpitdecks

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install 'cockpitdecks[xplane,loupedeck] @ git+https://github.com/dlicudi/cockpitdecks.git'
```

`cockpitdecks-configs` is not a Python package and should not be installed with `pip`.

## Releasing a pack

```sh
python scripts/release-deck.py release cirrus-sr22
python scripts/release-deck.py release cirrus-sr22 --execute
```

See each aircraft `README.md` for aircraft-specific notes.
