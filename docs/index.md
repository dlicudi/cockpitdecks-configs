---
title: Home
---

# Aircraft-ready deck layouts for X-Plane and Cockpitdecks

This repository collects practical, flyable deck configurations for real aircraft workflows.
It is built around X-Plane and tested primarily on the Loupedeck Live.

[Get Started](getting-started/installation.md){ .md-button .md-button--primary }
[Browse Aircraft](decks/index.md){ .md-button }

---

<div class="grid cards" markdown>

-   :material-airplane-takeoff: **Designed to fly**

    Pages are structured around real in-cockpit tasks: autopilot, engine, radios, transponder,
    PFI, pedestal, weather, and aircraft-specific control panels.

-   :material-dialpad: **Optimised for hardware**

    Development and testing focuses on the Loupedeck Live, while many patterns can be re-used
    on other supported decks.

-   :material-file-cog: **Config-first workflow**

    `cockpitdecks-configs` is configuration data, not a Python package. Install Cockpitdecks
    with `pip`, then clone this repository and link the aircraft deckconfigs you want to use.

</div>

## Quick Start

<div class="grid cards" markdown>

-   **:material-numeric-1-circle: Install Cockpitdecks**

    Use `pip` to install the Cockpitdecks build and extras that match your simulator and deck.

-   **:material-numeric-2-circle: Clone Configs**

    Clone this repository locally and keep the aircraft configs under version control.

-   **:material-numeric-3-circle: Link an Aircraft**

    Symlink the chosen `deckconfig` into the matching X-Plane aircraft folder and start flying.

</div>

[Installation Guide](getting-started/installation.md){ .md-button .md-button--primary }
[Development Notes](getting-started/development.md){ .md-button }

## Compatibility

!!! warning "Cockpitdecks build"
    These configs are developed and tested primarily with the [dlicudi/cockpitdecks](https://github.com/dlicudi/cockpitdecks) fork.

    Use that fork unless a specific aircraft page says otherwise.

