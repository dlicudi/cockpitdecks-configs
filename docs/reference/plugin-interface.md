# Plugin Helper Interface (PI_CockpitdecksFMSBrowser)

G1000-style FMS layout expects the following datarefs and commands.

## Current (used by fpl, nav, load)

### fms_browser (plan browser / LOAD)
- `plan_name`, `plan_filename`, `plan_departure`, `plan_destination`
- `plan_distance_nm`, `plan_waypoint_count`
- `plan_dep_runway`, `plan_dest_runway`, `plan_sid`, `plan_star`
- `index`, `count`, `status`
- `loaded_distance_nm` — total distance of loaded route (nm)
- Commands: `previous`, `next`, `load`, `refresh`

### fms_browser (live FMS)
- `fms_active_ident`, `fms_active_index`, `fms_active_altitude`
- `fms_first_ident`, `fms_last_ident`
- `fms_entry_count`

### fms_legs (FPL waypoint list)
- `row_1_index`, `row_1_ident`, `row_1_alt`, `row_1_is_active`, `row_1_is_selected`, `row_1_status`
- (same for row_2, row_3)
- `selected_index`, `entry_count`, `snapshot`, `window_start` (read=page 1,2,3…; writable=set page)
- Commands: `scroll_up`, `scroll_down` — move by **page** (1–3, 4–6, 7–9…), *not* 1-by-1
- Commands: `direct_to`, `select_row_1`, `select_row_2`, `select_row_3`, `clear_selected`

## Desired additions (for full G1000 parity)

### Per-waypoint in FPL (row_X_)
- `row_X_dtk` — desired track to that waypoint (°)
- `row_X_distance_nm` — distance to that waypoint (nm)

### NAV page
- `distance_to_destination_nm` — remaining distance to last waypoint
- `ete_to_destination_min` — ETE to destination
- `nav_source` — "GPS" | "VLOC" (for SRC tile, future toggle)

### X-Plane datarefs used (verify existence)
- `sim/cockpit2/radios/indicators/gps_dme_distance_nm` — dist to next WPT
- `sim/cockpit2/radios/indicators/gps_dme_time_min` — ETE to next WPT
- `sim/cockpit2/radios/indicators/gps_bearing_deg_mag` — DTK
- `sim/cockpit2/radios/indicators/gps_nav_bearing_deg_mag` — BRG to WPT
- `sim/cockpit/radios/gps_course_deviation` — XTK (nm)
- `sim/cockpit2/gauges/indicators/ground_speed_kt`
- `sim/cockpit2/gauges/indicators/ground_track_mag_pilot`
- `sim/cockpit2/radios/indicators/fms1_act_eta_hour`, `fms1_act_eta_minute`
