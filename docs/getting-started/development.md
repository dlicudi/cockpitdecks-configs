# Development

How to create and modify aircraft deck configurations.

## Project structure

```text
cockpitdecks-configs/
├── decks/                      # Aircraft configurations
│   └── cirrus-sr22/
│       └── deckconfig/         # Symlinked into X-Plane aircraft folder
│           ├── config.yaml     # Aircraft-level config
│           ├── _docs.yaml      # Documentation metadata
│           └── loupedecklive1/ # Layout for a specific deck
│               ├── config.yaml # Layout defaults (fonts, colours, home page)
│               ├── index.yaml  # Home page
│               ├── engine.yaml # Functional pages
│               └── encoders/   # Encoder sub-pages
├── modules/                    # Reusable page configs (radio, engine, etc.)
├── decktypes/                  # Deck type YAML definitions
├── scripts/                    # Doc generation scripts
└── mkdocs.yml
```

## Config hierarchy

Configs follow a hierarchy: **Aircraft → Layout → Page → Button**.

### Aircraft config

The top-level `config.yaml` in each `deckconfig/` folder defines the aircraft
and which decks it supports:

```yaml
aircraft: Cirrus SR22
icao: SR22
decks:
  loupedeck1:
    type: LoupedeckLive
    layout: loupedecklive1
    brightness: 80
```

It can also include global dataref rounding settings to reduce WebSocket churn.

### Layout config

Each layout folder (e.g. `loupedecklive1/`) contains its own `config.yaml`
with display defaults:

```yaml
default-label-font: DIN Condensed
default-label-size: 14
default-label-color: white
default-label-position: ct
default-home-page-name: index
```

### Page files

Each `.yaml` file in the layout folder defines a page of buttons. Pages can
include shared modules and encoder sub-pages:

```yaml
name: switches
includes: pager, encoders/encoders_fcu
buttons:
  - index: 0
    type: push
    command: sim/electrical/battery_1_toggle
    label: "BAT"
    formula: ${sim/cockpit2/electrical/battery_on[0]}
```

### Button types

| Type | Description |
|------|-------------|
| `page` | Navigates to another page |
| `push` | Single command on press |
| `begin-end-command` | Command on press and release (for multi-position switches) |
| `none` | Display only, no interaction |

Buttons use `formula` with `${dataref}` syntax to read live state from X-Plane.

## Adding a new aircraft

1. Create a folder under `decks/` matching the X-Plane aircraft directory name
2. Add a `deckconfig/` folder with a `config.yaml`
3. Create a layout folder for your deck (e.g. `loupedecklive1/`)
4. Add a layout `config.yaml` with display defaults
5. Add page `.yaml` files for each cockpit function
6. Symlink `deckconfig/` into the X-Plane aircraft folder

!!! tip
    Start by copying an existing aircraft config with a similar cockpit.
    The Cessna 172 SP is a good starting point for GA aircraft.

## Using modules

Modules are reusable button sets shared across aircraft. They live in the
`modules/` directory, organised by deck type:

```text
modules/
├── loupedecklive/    # Loupedeck Live modules
└── streamdeckxl/     # Stream Deck XL modules
```

Include a module in a page with the `includes` directive:

```yaml
includes: pager, encoders/encoders_fcu
```

See [Modules](../modules/modules.md) for the full list.

## Generating docs

The deck overview pages under `docs/decks/` are auto-generated. After modifying
configs, regenerate them:

```sh
python3 scripts/generate_deck_docs.py
```

!!! warning
    Do not manually edit files under `docs/decks/` — they will be overwritten.
    Edit the source configs or `_docs.yaml` instead.

To preview the docs site locally:

```sh
mkdocs serve
```

## VS Code YAML support

Use the MkDocs schema for `mkdocs.yml` and allow the custom YAML tags used by
Material for MkDocs.

```json title="settings.json"
{
  "yaml.schemas": {
    "https://squidfunk.github.io/mkdocs-material/schema.json": "mkdocs.yml"
  },
  "yaml.customTags": [
    "!ENV scalar",
    "!ENV sequence",
    "!relative scalar",
    "tag:yaml.org,2002:python/name:material.extensions.emoji.to_svg",
    "tag:yaml.org,2002:python/name:material.extensions.emoji.twemoji",
    "tag:yaml.org,2002:python/name:pymdownx.superfences.fence_code_format"
  ]
}
```
