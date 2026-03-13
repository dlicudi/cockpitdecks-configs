---
title: Home
---

<div class="cdx-hero">
  <div class="cdx-hero__copy">
    <p class="cdx-eyebrow">Cockpitdecks Configs</p>
    <h1>Aircraft-ready deck layouts for X-Plane and Cockpitdecks</h1>
    <p class="cdx-lead">
      This repository collects practical, flyable deck configurations for real aircraft workflows.
      It is built around X-Plane and tested primarily on the Loupedeck Live.
    </p>
    <div class="cdx-actions">
      <a class="md-button md-button--primary" href="getting-started/installation/">Get Started</a>
      <a class="md-button" href="decks/">Browse Aircraft</a>
    </div>
  </div>
  <div class="cdx-hero__visual">
    <img src="./assets/images/cirrus-sr22/cirrus-sr22-cockpit.png" alt="Cirrus SR22 cockpit overview" />
  </div>
</div>

<div class="cdx-section">
  <div class="cdx-grid cdx-grid--three">
    <div class="cdx-panel">
      <h2>Designed to fly</h2>
      <p>
        Pages are structured around real in-cockpit tasks: autopilot, engine, radios, transponder,
        PFI, pedestal, weather, and aircraft-specific control panels.
      </p>
    </div>
    <div class="cdx-panel">
      <h2>Optimised for hardware</h2>
      <p>
        Development and testing focuses on the Loupedeck Live, while many patterns can be re-used
        on other supported decks.
      </p>
    </div>
    <div class="cdx-panel">
      <h2>Config-first workflow</h2>
      <p>
        `cockpitdecks-configs` is configuration data, not a Python package. Install Cockpitdecks
        with `pip`, then clone this repository and link the aircraft deckconfigs you want to use.
      </p>
    </div>
  </div>
</div>

## Supported Aircraft

<div class="cdx-grid cdx-grid--cards">
  <a class="cdx-card" href="decks/cessna-172-sp/">
    <img src="./assets/images/cessna-172-sp/cessna-172-sp.png" alt="Cessna 172 SP" />
    <div class="cdx-card__body">
      <h3>Cessna 172 SP</h3>
      <p>Core GA workflow with radios, engine, transponder, weather, and G1000-style pages.</p>
    </div>
  </a>
  <a class="cdx-card" href="decks/cirrus-sr22/">
    <img src="./assets/images/cirrus-sr22/cirrus-sr22.png" alt="Cirrus SR22" />
    <div class="cdx-card__body">
      <h3>Cirrus SR22</h3>
      <p>G1000-oriented layout with FCU, GCU478, PFI, transponder, weather, and system pages.</p>
    </div>
  </a>
  <a class="cdx-card" href="decks/beechcraft-baron-58/">
    <img src="./assets/images/beechcraft-baron-58/beechcraft-baron-58.png" alt="Beechcraft Baron 58" />
    <div class="cdx-card__body">
      <h3>Beechcraft Baron 58</h3>
      <p>Twin-engine focus with dedicated engine and aircraft-system coverage.</p>
    </div>
  </a>
  <a class="cdx-card" href="decks/lancair-evolution/">
    <img src="./assets/images/lancair-evolution/lancair-evolution-banner.jpg" alt="Lancair Evolution" />
    <div class="cdx-card__body">
      <h3>Lancair Evolution</h3>
      <p>Glass-cockpit workflow with G1000-style navigation, audio, weather, and systems pages.</p>
    </div>
  </a>
  <a class="cdx-card" href="decks/toliss-airbus-A321-neo/">
    <img src="./assets/images/Loupedeck_live.png" alt="ToLiss Airbus A321 NEO" />
    <div class="cdx-card__body">
      <h3>ToLiss Airbus A321 NEO</h3>
      <p>Airliner-oriented layouts for cockpit flows that differ substantially from GA aircraft.</p>
    </div>
  </a>
  <a class="cdx-card" href="decks/aerobask-robin-dr401/">
    <img src="./assets/images/aerobask-robin-dr401/pfi.png" alt="Aerobask Robin DR401" />
    <div class="cdx-card__body">
      <h3>Aerobask Robin DR401</h3>
      <p>Another light-aircraft reference layout with practical examples you can adapt.</p>
    </div>
  </a>
</div>

## Quick Start

<div class="cdx-grid cdx-grid--three">
  <div class="cdx-step">
    <span>1</span>
    <h3>Install Cockpitdecks</h3>
    <p>Use `pip` to install the Cockpitdecks build and extras that match your simulator and deck.</p>
  </div>
  <div class="cdx-step">
    <span>2</span>
    <h3>Clone Configs</h3>
    <p>Clone this repository locally and keep the aircraft configs under version control.</p>
  </div>
  <div class="cdx-step">
    <span>3</span>
    <h3>Link an Aircraft</h3>
    <p>Symlink the chosen `deckconfig` into the matching X-Plane aircraft folder and start flying.</p>
  </div>
</div>

[Installation Guide](getting-started/installation.md){ .md-button .md-button--primary }
[Development Notes](getting-started/development.md){ .md-button }

## Compatibility

!!! warning "Cockpitdecks build"
    These configs are developed and tested primarily with the [dlicudi/cockpitdecks](https://github.com/dlicudi/cockpitdecks) fork.
    
    Use that fork unless a specific aircraft page says otherwise.

## Examples

<div class="cdx-grid cdx-grid--gallery">
  <figure class="cdx-shot">
    <img src="./assets/images/cirrus-sr22/home.png" alt="Cirrus SR22 home page" />
    <figcaption>Home</figcaption>
  </figure>
  <figure class="cdx-shot">
    <img src="./assets/images/cirrus-sr22/pfi.png" alt="Cirrus SR22 primary flight instruments page" />
    <figcaption>PFI</figcaption>
  </figure>
  <figure class="cdx-shot">
    <img src="./assets/images/cirrus-sr22/engine.png" alt="Cirrus SR22 engine page" />
    <figcaption>Engine</figcaption>
  </figure>
  <figure class="cdx-shot">
    <img src="./assets/images/cirrus-sr22/transponder.png" alt="Cirrus SR22 transponder page" />
    <figcaption>Transponder</figcaption>
  </figure>
</div>

## Notes

- The `Examples` section documents stable patterns already in use in configs.
- The `Experimental` section documents custom extensions and prototype behaviours that may require the `dlicudi/cockpitdecks` fork.
