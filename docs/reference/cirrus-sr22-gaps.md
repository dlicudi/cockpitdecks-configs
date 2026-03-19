# Cirrus SR22 — Missing Functions / Datarefs / Commands

Gap analysis based on the Laminar Cirrus SR22 aircraft files (`SR22.systems.lua`, `SR22_cockpit.obj`, `Cirrus SR22.acf`) vs. the current loupedecklive1 config.

## Currently implemented ✓

| Category | Implemented |
|----------|-------------|
| **Switches** | IGNITION, AVIONICS, BAT 1/2, ALT 1/2, PARK BRAKE, FUEL OFF/LEFT/RIGHT, SWITCHES 2 |
| **Switches2 (Lights & Icing)** | NAV, STROBE, LAND, ICE lights; PITOT, ICE PROTECT, PUMP BKUP, NORM/HIGH, PROP, WSHLD |
| **Fuel** | `laminar/sr22/fuel_sel_left_off`, `fuel_sel_left_select`, `fuel_sel_right_select` |
| **Icing** | `laminar/sr22/switch/ice_protect_*` commands; `sim/ice/tks_bkup_*` commands |

---

## Missing — SR22-specific commands

### Sun visors
| Command | Description |
|--------|-------------|
| `laminar/sr22/sunvisor_left_up` | Sun visor left up |
| `laminar/sr22/sunvisor_left_dn` | Sun visor left down |
| `laminar/sr22/sunvisor_right_up` | Sun visor right up |
| `laminar/sr22/sunvisor_right_dn` | Sun visor right down |

**Datarefs:** `laminar/sr22/sun_visor_left`, `laminar/sr22/sun_visor_right` (1=down, 0=neutral, -1=stowed)

### Climate / ventilation
| Command | Description |
|--------|-------------|
| `laminar/sr22/fan_speed_right` | Increase cabin fan speed |
| `laminar/sr22/fan_speed_left` | Decrease cabin fan speed |
| `laminar/sr22/button/air_con_toggle` | Air conditioning toggle |

**Dataref:** `laminar/sr22/climate_fan_speed` (0–3)

### Fuel selector (rotary)
| Command | Description |
|--------|-------------|
| `laminar/sr22/fuel_sel_left` | Rotate fuel selector left (OFF←LEFT←RIGHT) |
| `laminar/sr22/fuel_sel_right` | Rotate fuel selector right (OFF→LEFT→RIGHT) |

*Note: Config uses direct-position commands (`fuel_sel_left_off`, `fuel_sel_left_select`, etc.) which are already implemented.*

### TKS anti-ice (additional)
| Command | Description |
|--------|-------------|
| `laminar/sr22/anti_ice_tks_max` | TKS MAX (hold for max flow) |
| `laminar/sr22/switch/ice_protect_on` | TKS ON |
| `laminar/sr22/switch/ice_protect_off` | TKS OFF |
| `laminar/sr22/switch/ice_protect_norm` | TKS NORM |
| `laminar/sr22/switch/ice_protect_high` | TKS HIGH |

*Config uses `commands` for ice_protect (on/off), ice_norm_high (norm/high), and PUMP BKUP (`sim/ice/tks_bkup_on`, `sim/ice/tks_bkup_off`) to avoid read-only dataref write errors.*

### Boost pump
| Command | Description |
|--------|-------------|
| `laminar/sr22/switch/boost_pump_up` | Boost pump ON |
| `laminar/sr22/switch/boost_pump_dn` | Boost pump OFF |

**Dataref:** `laminar/sr22/switch/boost_pump` (writable, 0 or 1)

---

## Missing — Interior lights (SR22 uses sim datarefs)

From `SR22.systems.lua`:

| Dataref | SR22 use |
|---------|----------|
| `sim/cockpit2/switches/generic_lights_switch[4]` | Dome light |
| `sim/cockpit2/switches/generic_lights_switch[6]` | Flood light |
| `sim/cockpit2/switches/generic_lights_switch[0]` | Reading light 1 |
| `sim/cockpit2/switches/generic_lights_switch[1]` | Reading light 2 |
| `sim/cockpit2/switches/generic_lights_switch[10]` | Edge lighting |
| `sim/cockpit2/switches/generic_lights_switch[11]` | Wingtip LIT force |

**Commands:** Use `sim/lights/generic_0X_light_tog` for indices 0–11, or `sim/cockpit2/switches/generic_lights_switch` via set-dataref.

*Current config:* switches2 uses `generic_01_light_tog` for ICE light (index 0). Dome, flood, reading, edge, wingtip are not mapped.

---

## Missing — Annunciators (read-only, for status display)

| Dataref | Description |
|---------|-------------|
| `laminar/sr22/annunciators/com` | COM annunciator |
| `laminar/sr22/annunciators/nav` | NAV annunciator |
| `laminar/sr22/annunciators/crs` | CRS annunciator |
| `laminar/sr22/annunciators/xpdr` | XPDR annunciator |
| `laminar/sr22/annunciators/flaps_up` | Flaps up |
| `laminar/sr22/annunciators/flaps_50` | Flaps 50% |
| `laminar/sr22/annunciators/flaps_100` | Flaps 100% |
| `laminar/sr22/annunciators/o2_full` … `o2_empty` | O2 bottle pressure annunciators |
| `laminar/sr22/annunciators/audio/*` | Audio panel (COM1/2, NAV1/2, MKR, etc.) |
| `laminar/sr22/annunciators/ap/*` | Autopilot (AP, FD, LVL, APR, NAV, HDG, FLC, VNV, VS, ALT) |
| `laminar/sr22/annunciators/air_con` | Air conditioning |

*Use case:* Status or annunciator pages; not currently wired in loupedecklive1.

---

## Missing — Landing lights (left/right)

SR22 uses:
- `sim/cockpit2/switches/landing_lights_switch[0]` — master (currently used as LAND)
- `sim/cockpit2/switches/landing_lights_switch[1]` — left
- `sim/cockpit2/switches/landing_lights_switch[2]` — right

**Commands:** `sim/lights/landing_01_light_tog`, `sim/lights/landing_02_light_tog`, `sim/lights/landing_03_light_tog` (or similar indices).

---

## Suggested additions (by priority)

| Priority | Item | Page | Notes |
|----------|------|------|-------|
| **High** | Boost pump | switches | `laminar/sr22/switch/boost_pump_up` / `boost_pump_dn` or set-dataref |
| **High** | TKS MAX | switches2 | `laminar/sr22/anti_ice_tks_max` (hold for max) |
| **Medium** | Dome, flood, reading lights | switches2 or lights | `generic_lights_switch[4,6,0,1]` |
| **Medium** | Climate fan | new page or index | `laminar/sr22/fan_speed_right` / `fan_speed_left` |
| **Medium** | Air conditioning | new page or index | `laminar/sr22/button/air_con_toggle` |
| **Low** | Sun visors | new page | `laminar/sr22/sunvisor_*` |
| **Low** | Landing L/R | switches2 | Separate left/right landing lights |
| **Low** | Annunciators | status page | Read-only for display |

---

## Reference: SR22 fuel selector positions

- `0` = OFF (left off)
- `1` = LEFT
- `2` = RIGHT
- `3` = OFF (right off)

Commands `fuel_sel_left_off|fuel_sel_left_select|fuel_sel_right_select|fuel_sel_right_off` set these positions directly.
