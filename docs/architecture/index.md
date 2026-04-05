---
title: Architecture
---

# Architecture

This page is the shortest useful map of how `cockpitdecks-configs` itself is
put together.

It is intended for two audiences:

- humans trying to understand where behaviour comes from
- AI agents that need repository context before making changes

## What this repository is

`cockpitdecks-configs` is a configuration repository.

It is **not** the Cockpitdecks runtime itself. The Python application, deck
drivers, and simulator integration live in the Cockpitdecks project. This
repository provides aircraft-specific and deck-specific YAML configuration that
the runtime consumes.

That separation matters:

- if you are changing **layout, labels, page structure, commands, formulas, or reusable modules**, edit this repo
- if you are changing **runtime behaviour, parsing, device support, rendering logic, or simulator transport**, that likely belongs in Cockpitdecks, not here

## Repository boundaries

Within the broader Cockpitdecks ecosystem, this repository sits in the config
layer. At a high level the local boundary looks like this:

1. **Cockpitdecks runtime**
   Reads deck configuration, talks to X-Plane, evaluates formulas, and renders
   controls on hardware.
2. **This repository**
   Supplies aircraft configs, reusable modules, deck type definitions, and
   documentation sources.
3. **X-Plane aircraft installation**
   Receives a symlinked `deckconfig/` folder for a specific aircraft.
4. **Documentation**
   MkDocs publishes the hand-written docs, while aircraft-specific notes live in
   each aircraft `README.md`.

## Repository map

```text
cockpitdecks-configs/
├── decks/           # Aircraft source configs
├── modules/         # Reusable config fragments shared across aircraft
├── decktypes/       # Deck capability/type definitions
├── docs/            # Hand-written documentation
├── scripts/         # Support scripts
└── mkdocs.yml       # Docs site navigation and configuration
```

## Source of truth

Not every file in this repository should be edited directly.

| Path | Role | Edit directly? |
|---|---|---|
| `decks/<aircraft>/deckconfig/` | Primary aircraft configuration source | Yes |
| `decks/<aircraft>/README.md` | Aircraft-specific notes | Yes |
| `modules/` | Reusable shared config source | Yes |
| `decktypes/` | Deck type definitions | Yes |
| `docs/architecture/`, `docs/reference/`, `docs/getting-started/` | Hand-written docs | Yes |

If a change is aircraft-specific, prefer the aircraft `README.md` or the config source rather than a separate generated docs page.

## Configuration hierarchy

The central model is:

**Aircraft -> Layout -> Page -> Button**

### Aircraft

Each aircraft lives under `decks/<aircraft>/deckconfig/`.

The top-level files define aircraft metadata and which hardware layouts exist
for that aircraft.

Important files:

- `config.yaml`: aircraft-level config and deck registrations
- `README.md`: aircraft-specific notes and usage details

### Layout

Each supported hardware layout gets its own directory such as
`loupedecklive1/`, `streamdeckxl1/`, or `panels/`.

Layout config typically defines:

- deck defaults
- typography and colour defaults
- home page
- layout-specific shared includes

### Page

Each page is a YAML file inside the layout directory.

A page defines:

- its name
- included modules or encoder fragments
- the button grid or panel controls for that page

### Button

Buttons are the smallest functional unit.

A button typically combines:

- an interaction type such as `push`, `page`, or `begin-end-command`
- simulator commands
- display labels/icons
- formulas reading simulator state through datarefs

## Reuse model

Reuse happens in three main ways:

- **modules**: shared page fragments used across multiple aircraft
- **layout defaults**: shared display defaults within one hardware layout
- **local documentation**: `README.md` keeps aircraft notes close to the operational config

This means most work should begin by deciding whether a change is:

- aircraft-specific
- deck-specific
- reusable across several aircraft

That decision determines whether the edit belongs in `decks/`, `modules/`, or a
script.

## Documentation architecture

The docs site is intentionally small:

- hand-written docs for setup, architecture, and shared reference
- aircraft-specific notes in each aircraft `README.md`

## Change guide

Use this table as a shortcut before editing:

| If you want to change... | Start here |
|---|---|
| aircraft pages, commands, labels, formulas | `decks/<aircraft>/deckconfig/<layout>/` |
| reusable radio/engine/G1000 content | `modules/` |
| deck hardware capabilities or mappings | `decktypes/` |
| docs navigation or published section structure | `mkdocs.yml` |
| aircraft-specific notes | `decks/<aircraft>/README.md` |
| conceptual docs for humans and agents | `docs/architecture/` or `docs/reference/` |

## Working rules for agents

If you are an AI agent operating in this repository:

1. Treat `decks/`, `modules/`, and `decktypes/` as primary sources.
2. Treat hand-written docs and aircraft `README.md` files as the source material.
3. Check `mkdocs.yml` before adding a new documentation section.
4. Prefer updating the source config or generator when the same issue appears in
   multiple aircraft pages.
5. Do not infer runtime behaviour from this repo alone when the question is
   really about Cockpitdecks internals.

## Scope note

This page is intentionally limited to the configuration repository.

System-level Cockpitdecks architecture, runtime flow, and multi-repository
workspace mapping belong with the Cockpitdecks runtime repository rather than
the config repository docs.

## Related pages

- [Development](../getting-started/development.md)
- [Reference](../reference/index.md)
- [Modules](../modules/modules.md)
