# Cirrus SR22 Aircraft Reference

Reference document for the **Laminar Research Cirrus SR22** (X-Plane 12 default aircraft). Derived from the aircraft files: `Cirrus SR22.acf`, `plugins/xlua/scripts/SR22.systems/SR22.systems.lua`.

Use this document when building cockpit deck configurations for the SR22.

---

## Source Files

| Path | Purpose |
|------|---------|
| `X-Plane 12/Aircraft/Laminar Research/Cirrus SR22/Cirrus SR22.acf` | Aircraft definition (geometry, properties) |
| `plugins/xlua/scripts/SR22.systems/SR22.systems.lua` | Systems logic, custom datarefs, custom commands |

---

## Custom Datarefs (`laminar/sr22/*`)

### Sun visors
| Dataref | Type | Values |
|---------|------|--------|
| `laminar/sr22/sun_visor_left` | number | 1 = down, 0 = neutral, -1 = stowed |
| `laminar/sr22/sun_visor_right` | number | 1 = down, 0 = neutral, -1 = stowed |

### Fuel & boost pump
| Dataref | Type | Values |
|---------|------|--------|
| `laminar/sr22/fuel_selector_pos` | number | 0 = left off, 1 = left select, 2 = right select, 3 = right off |
| `laminar/sr22/switch/boost_pump` | number | 0 = off, 1 = boost, -1 = prime (momentary) |

### Climate
| Dataref | Type | Values |
|---------|------|--------|
| `laminar/sr22/climate_fan_speed` | number | 0 = off, 1–3 = fan speed |

### Ice protection (TKS)
| Dataref | Type | Values |
|---------|------|--------|
| `laminar/sr22/switch/ice_protect` | number | 0 = off, 1 = on |
| `laminar/sr22/switch/ice_norm_high` | number | 0 = norm, 1 = high |
| `laminar/sr22/switch/ice_max` | number | 0–1 (animates during TKS MAX hold) |

### Annunciators — GCU input
| Dataref | Type |
|---------|------|
| `laminar/sr22/annunciators/com` | number |
| `laminar/sr22/annunciators/nav` | number |
| `laminar/sr22/annunciators/crs` | number |
| `laminar/sr22/annunciators/xpdr` | number |

### Annunciators — Flaps
| Dataref | Type |
|---------|------|
| `laminar/sr22/annunciators/flaps_up` | number |
| `laminar/sr22/annunciators/flaps_50` | number |
| `laminar/sr22/annunciators/flaps_100` | number |

### Annunciators — Oxygen
| Dataref | Type |
|---------|------|
| `laminar/sr22/annunciators/o2_full` | number |
| `laminar/sr22/annunciators/o2_1600` | number |
| `laminar/sr22/annunciators/o2_1200` | number |
| `laminar/sr22/annunciators/o2_800` | number |
| `laminar/sr22/annunciators/o2_400` | number |
| `laminar/sr22/annunciators/o2_empty` | number |
| `laminar/sr22/annunciators/o2_req` | number |
| `laminar/sr22/annunciators/o2_fault` | number |

### Annunciators — Audio panel
| Dataref | Type |
|---------|------|
| `laminar/sr22/annunciators/audio/mkr_mute` | number |
| `laminar/sr22/annunciators/audio/com1` | number |
| `laminar/sr22/annunciators/audio/com2` | number |
| `laminar/sr22/annunciators/audio/nav1` | number |
| `laminar/sr22/annunciators/audio/nav2` | number |
| `laminar/sr22/annunciators/audio/mic1` | number |
| `laminar/sr22/annunciators/audio/mic2` | number |
| `laminar/sr22/annunciators/audio/pilot` | number |
| `laminar/sr22/annunciators/audio/coplt` | number |
| `laminar/sr22/annunciators/audio/pass` | number |

### Annunciators — Autopilot
| Dataref | Type |
|---------|------|
| `laminar/sr22/annunciators/ap/ap` | number |
| `laminar/sr22/annunciators/ap/fd` | number |
| `laminar/sr22/annunciators/ap/lvl` | number |
| `laminar/sr22/annunciators/ap/apr` | number |
| `laminar/sr22/annunciators/ap/nav` | number |
| `laminar/sr22/annunciators/ap/hdg` | number |
| `laminar/sr22/annunciators/ap/flc` | number |
| `laminar/sr22/annunciators/ap/vnv` | number |
| `laminar/sr22/annunciators/ap/vs` | number |
| `laminar/sr22/annunciators/ap/alt` | number |
| `laminar/sr22/annunciators/air_con` | number |

### Read-write (animation / control)
| Dataref | Type | Notes |
|---------|------|-------|
| `laminar/sr22/dome_light_rot_x-1` … `-4` | number | Dome light rotation X |
| `laminar/sr22/dome_light_rot_y-1` … `-4` | number | Dome light rotation Y |
| `laminar/sr22/eyeball_vent_rot_x-1` … `-4` | number | Eyeball vent rotation X |
| `laminar/sr22/eyeball_vent_rot_y-1` … `-4` | number | Eyeball vent rotation Y |
| `laminar/sr22/alt_air_pull` | number | Alternate air pull |
| `laminar/sr22/temp_control` | number | Climate temperature control |
| `laminar/sr22/knobs/parking_brake_valve_anim` | number | Parking brake valve animation (0–1) |

---

## Custom Commands (`laminar/sr22/*`)

### Sun visors
| Command | Description |
|---------|-------------|
| `laminar/sr22/sunvisor_left_up` | Sun visor left up |
| `laminar/sr22/sunvisor_left_dn` | Sun visor left down |
| `laminar/sr22/sunvisor_right_up` | Sun visor right up |
| `laminar/sr22/sunvisor_right_dn` | Sun visor right down |

### Fuel selector
| Command | Description |
|---------|-------------|
| `laminar/sr22/fuel_sel_left` | Rotate fuel selector left |
| `laminar/sr22/fuel_sel_right` | Rotate fuel selector right |
| `laminar/sr22/fuel_sel_left_off` | Set fuel selector to left off (position 0) |
| `laminar/sr22/fuel_sel_left_select` | Set fuel selector to left select (position 1) |
| `laminar/sr22/fuel_sel_right_select` | Set fuel selector to right select (position 2) |
| `laminar/sr22/fuel_sel_right_off` | Set fuel selector to right off (position 3) |

### Climate
| Command | Description |
|---------|-------------|
| `laminar/sr22/fan_speed_right` | Increase fan speed |
| `laminar/sr22/fan_speed_left` | Decrease fan speed |
| `laminar/sr22/button/air_con_toggle` | Air conditioning toggle |

### Ice protection (TKS)
| Command | Description |
|---------|-------------|
| `laminar/sr22/anti_ice_tks_max` | TKS MAX (hold for max flow) |
| `laminar/sr22/switch/ice_protect_on` | TKS ON |
| `laminar/sr22/switch/ice_protect_off` | TKS OFF |
| `laminar/sr22/switch/ice_protect_norm` | TKS NORM |
| `laminar/sr22/switch/ice_protect_high` | TKS HIGH |

### Boost pump
| Command | Description |
|---------|-------------|
| `laminar/sr22/switch/boost_pump_up` | Boost pump switch up (ON) |
| `laminar/sr22/switch/boost_pump_dn` | Boost pump switch down (OFF / prime on hold) |
| `laminar/sr22/switch/boost_pump_boost` | Set boost pump to boost (simpit) |
| `laminar/sr22/switch/boost_pump_off` | Set boost pump to off (simpit) |
| `laminar/sr22/switch/boost_pump_prime` | Set boost pump to prime (simpit) |

---

## Sim Datarefs Used by SR22

### Lights (generic_lights_switch)
| Index | SR22 use |
|-------|----------|
| 0 | Reading light 1 |
| 1 | Reading light 2 |
| 4 | Dome light |
| 6 | Flood light |
| 10 | Edge lighting |
| 11 | Wingtip LIT force |

### Other sim datarefs
| Dataref | SR22 use |
|---------|----------|
| `sim/cockpit2/switches/instrument_brightness_ratio[1]` | G1000 screen brightness |
| `sim/cockpit2/switches/instrument_brightness_ratio[3]` | G1000 bezel brightness |
| `sim/cockpit2/switches/instrument_brightness_ratio[4]` | Indicator lights |
| `sim/cockpit2/switches/landing_lights_switch[0]` | Landing lights master |
| `sim/cockpit2/switches/landing_lights_switch[1]` | Landing light left |
| `sim/cockpit2/switches/landing_lights_switch[2]` | Landing light right |
| `sim/cockpit2/ice/ice_surface_tks_left_on` | TKS wing left |
| `sim/cockpit2/ice/ice_surface_tks_right_on` | TKS wing right |
| `sim/cockpit2/ice/ice_prop_tks_on_per_engine[0]` | TKS prop |
| `sim/flightmodel2/controls/flap1_deploy_ratio` | Flaps (0, 0.5, 1) |
| `sim/cockpit2/controls/park_brake_valve` | Parking brake |

---

## Sim Commands Used by SR22

| Command | Description |
|---------|-------------|
| `sim/ice/tks_max` | TKS max flow (called by `laminar/sr22/anti_ice_tks_max`) |

---

## Fuel Selector Mapping

| `laminar/sr22/fuel_selector_pos` | `sim/cockpit2/fuel/fuel_tank_selector` | Physical position |
|----------------------------------|----------------------------------------|-------------------|
| 0 | 0 | Left off |
| 1 | 1 | Left select |
| 2 | 3 | Right select |
| 3 | 0 | Right off |

---

## Related Documents

- [cirrus-sr22-gaps.md](./cirrus-sr22-gaps.md) — Gap analysis vs. current loupedecklive1 config
