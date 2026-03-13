# Installation

## Python
[python.org](https://www.python.org/)

1. Download Python 3.10 or newer from https://www.python.org/downloads/
2. Install it and confirm `python3` is available in your shell


## XPPython

[XPPython3 documentation](https://xppython3.readthedocs.io/en/latest/index.html)

1. Download XPPython3 zipfile
2. Extract the xp3xxx zip into `X-Plane/Resources/plugins`
3. On macOS, follow the quarantine steps: https://xppython3.readthedocs.io/en/latest/usage/mac_quarantine.html
4. Start X-Plane once to confirm the plugin loads

### X-Plane plugin

Cockpitdecks also requires the main X-Plane plugin `PI_cockpitdecks.py` to be present and enabled in:

```text
X-Plane/Resources/plugins/PythonPlugins/
```

This is the active Cockpitdecks X-Plane integration. Older helper plugin references are obsolete for the normal installation flow.


## Cockpitdecks
You can also refer to the upstream documentation here: https://devleaks.github.io/cockpitdecks-docs/Installation/

### Create a virtual environment

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

### Install cockpitdecks

For a typical X-Plane and Loupedeck setup:

```sh
pip install 'cockpitdecks[xplane,loupedeck] @ git+https://github.com/dlicudi/cockpitdecks.git'
```

If you want an editable local checkout instead:

```sh
git clone https://github.com/dlicudi/cockpitdecks.git
cd cockpitdecks
pip install -e '.[xplane,loupedeck]'
```

Common extras:

- `xplane`: X-Plane simulator support
- `loupedeck`: Loupedeck Live / Live S / CT support
- `streamdeck`: Elgato Stream Deck support
- `xtouchmini`: Behringer X-Touch Mini support
- `weather`: weather icon support
- `toliss`: ToLiss aircraft extensions

### Install cockpitdecks-configs

`cockpitdecks-configs` is a data/config repository, not a Python package.

```sh
git clone https://github.com/dlicudi/cockpitdecks-configs.git
```

### Link an aircraft deckconfig

Link the aircraft you want to use into the matching X-Plane aircraft folder:

```sh
ln -s ~/GitHub/cockpitdecks-configs/decks/cirrus-sr22/deckconfig ~/X-Plane\ 12/Aircraft/Laminar\ Research/Cirrus\ SR22
```

Repeat that pattern for other aircraft by changing the source and destination paths.

### Start Cockpitdecks

Once X-Plane and XPPython3 are installed, start Cockpitdecks from your virtual environment:

```sh
cockpitdecks-cli
```

If you are working from a local editable checkout of `cockpitdecks`, run the same command from that environment after `pip install -e`.

For local development tips and VS Code launch examples, see [Development](development.md).
