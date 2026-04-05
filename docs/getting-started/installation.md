# Installation

## Prerequisites

| Component | Version | Link |
|-----------|---------|------|
| X-Plane | 12 | [x-plane.com](https://www.x-plane.com) |
| Python | 3.10+ | [python.org](https://www.python.org) |
| XPPython3 | Latest | [Documentation](https://xppython3.readthedocs.io/en/latest/index.html) |
| Deck hardware | Loupedeck Live, Stream Deck XL, or another supported deck | Check the aircraft README and Cockpitdecks runtime support |

## 1. Install XPPython3

1. Download the XPPython3 zip from the [XPPython3 site](https://xppython3.readthedocs.io/en/latest/index.html)
2. Extract into `X-Plane/Resources/plugins/`
3. Start X-Plane once to confirm the plugin loads

macOS note:
Follow the [quarantine steps](https://xppython3.readthedocs.io/en/latest/usage/mac_quarantine.html)
before first launch.

## 2. Install Cockpitdecks

Create a virtual environment and install Cockpitdecks with the extras that match your
simulator and deck hardware.

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

#### Loupedeck

```sh
pip install 'cockpitdecks[xplane,loupedeck] @ git+https://github.com/dlicudi/cockpitdecks.git'
```

#### Stream Deck

```sh
pip install 'cockpitdecks[xplane,streamdeck] @ git+https://github.com/dlicudi/cockpitdecks.git'
```

#### X-Touch Mini

```sh
pip install 'cockpitdecks[xplane,xtouchmini] @ git+https://github.com/dlicudi/cockpitdecks.git'
```

#### Editable (dev)

```sh
git clone https://github.com/dlicudi/cockpitdecks.git
cd cockpitdecks
pip install -e '.[xplane,loupedeck]'
```

Available extras:

| Extra | Description |
|-------|-------------|
| `xplane` | X-Plane simulator support |
| `loupedeck` | Loupedeck Live / Live S / CT |
| `streamdeck` | Elgato Stream Deck models |
| `xtouchmini` | Behringer X-Touch Mini |
| `weather` | Weather icon support |
| `toliss` | ToLiss aircraft extensions |

Combine extras as needed, e.g. `cockpitdecks[xplane,loupedeck,weather,toliss]`.

### X-Plane plugin

Cockpitdecks requires `PI_cockpitdecks.py` in:

```text
X-Plane/Resources/plugins/PythonPlugins/
```

This file is included with the Cockpitdecks install.

## 3. Clone cockpitdecks-configs

`cockpitdecks-configs` is configuration data, not a Python package — just clone it:

```sh
git clone https://github.com/dlicudi/cockpitdecks-configs.git
```

## 4. Link an aircraft

Symlink the aircraft `deckconfig` folder into the matching X-Plane aircraft directory:

```sh
ln -s /path/to/cockpitdecks-configs/decks/cirrus-sr22/deckconfig \
      ~/X-Plane\ 12/Aircraft/Laminar\ Research/Cirrus\ SR22/deckconfig
```

Repeat for other aircraft by changing the source and destination paths.

## 5. Start flying

With X-Plane running and XPPython3 loaded, start Cockpitdecks from your virtual environment:

```sh
cockpitdecks-cli
```

For additional detail, see the [Cockpitdecks documentation](https://devleaks.github.io/cockpitdecks-docs/Installation/).

For local development tips and VS Code launch configurations, see [Development](development.md).
