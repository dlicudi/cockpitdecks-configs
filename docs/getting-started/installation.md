# Installation

## Python
https://www.python.org/

1. Download Python https://www.python.org/downloads/
2. Install


## XPPython

https://xppython3.readthedocs.io/en/latest/index.html

1. Download XPPython3 zipfile
2.  Extract the xp3xxx.zip into your `X-Plane/Resources/plugins`
3.  Follow steps for MAC quarantine https://xppython3.readthedocs.io/en/latest/usage/mac_quarantine.html
4.  Start X-Plane


## Cockpitdecks
You can also follow installation instructions specific to cockpitdecks here: https://devleaks.github.io/cockpitdecks-docs/Installation/

### Python packages

Required packages:

```
pip install ruamel.yaml pillow
```

Weather/Metar button representation:

```
pip install avwx-engine scipy suntime timezonefinder
```

Streamdeck devices:

```
pip install streamdeck
```

Loupedeck devices:

```
pip install git+https://github.com/devleaks/python-loupedeck-live.git
```

Touch Mini devices:

```
pip install git+https://github.com/devleaks/python-berhinger-xtouchmini.git
```

### Download cockpitdecks

!!! warning experimental build
    *Supports some experimental features such as custom sides buttons, encoders with toggle for step changes and improved EncoderValue class.*

=== "Original"
    ```
    git checkout https://github.com/devleaks/cockpitdecks.git
    ```

=== "Experimental"
    ```
    git checkout https://github.com/dlicudi/cockpitdecks.git
    ```

### Cockpitdecks Helper Plugin

```
cp PI_cockpitdecks_helper.py ~/X-Plane\ 12/Resources/plugins/PythonPlugins/
```

### Cockpitdecks Configs

```
git checkout https://github.com/dlicudi/cockpitdecks-configs.git
```
