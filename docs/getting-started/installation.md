# Installation

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
