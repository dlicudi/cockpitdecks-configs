---
title: Home
---

# Aircraft-ready deck layouts for X-Plane and Cockpitdecks

This repository collects practical, flyable deck configurations for real aircraft workflows.
It is built around X-Plane and tested primarily on the Loupedeck Live.

**[Get Started](getting-started/installation.md)**

---

## Highlights

- **Designed to fly** — Pages are structured around real in-cockpit tasks: autopilot, engine, radios, transponder, PFI, pedestal, weather, and aircraft-specific control panels.
- **Optimised for hardware** — Development and testing focuses on the Loupedeck Live, while many patterns can be re-used on other supported decks.
- **Config-first workflow** — `cockpitdecks-configs` is configuration data, not a Python package. Install Cockpitdecks with `pip`, then clone this repository and link the aircraft deckconfigs you want to use.

## Quick Start

1. **Install Cockpitdecks** — Use `pip` to install the Cockpitdecks build and extras that match your simulator and deck.
2. **Clone Configs** — Clone this repository locally and keep the aircraft configs under version control.
3. **Link an Aircraft** — Symlink the chosen `deckconfig` into the matching X-Plane aircraft folder and start flying.

**[Installation Guide](getting-started/installation.md)** · [Development Notes](getting-started/development.md)

## Compatibility

!!! warning "Cockpitdecks build"
    These configs are developed and tested primarily with the [dlicudi/cockpitdecks](https://github.com/dlicudi/cockpitdecks) fork.

    Use that fork unless a specific aircraft page says otherwise.
