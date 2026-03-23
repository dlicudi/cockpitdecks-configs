# Plugin Helper Interface (PI_CockpitdecksFMSBrowser)

G1000-style FMS layout expects the following datarefs and commands.

## Current (used by `fms_fpl`, `fms_nav`, `fms_load` pages)

### fms_browser (plan browser / LOAD)

**3-row paged list (same paging model as `fms_legs` on FPL):** show plans 1–3, then 4–6, etc.

- `list_row_1_filename` … `list_row_3_filename` — file basename without `.fms`
- `list_row_1_timestamp` … `list_row_3_timestamp` — file timestamp label used on the LOAD page
- `list_row_1_index` … `list_row_3_index` — 1-based index of that row’s plan in the full sorted list (empty if row blank)
- `list_row_1_route` … `list_row_3_route` — departure / destination line for the row’s plan
- `list_row_1_wpt_count` … `list_row_3_wpt_count` — waypoint count in file
- `list_row_1_max_alt_ft` … `list_row_3_max_alt_ft` — max waypoint altitude in file (ft MSL; 0 if empty row)
- `list_row_1_distance_nm` … `list_row_3_distance_nm` — total great-circle distance along parsed route (nm)
- `list_row_1_is_selected` … `list_row_3_is_selected` — highlight when that row’s plan is selected
- `list_page` — e.g. `1/4` (current page / total pages)
- `list_sel_count` — which **visible row** (1–3) is selected on the current page, e.g. `2/3` or `-/3` when none; use `list_page` + row `list_row_*_index` for global plan order
- `list_sort_key` / `list_sort_mode` — `NAME` or `TIME`
- `list_sort_direction` — `ASC` or `DESC`
- `list_window_page` — int, 1-based visible page (for encoder / subscriptions; same paging as `list_scroll_*`)
- Commands: `list_scroll_up`, `list_scroll_down` — move by **one page** (three plans), not one-by-one (Loupedeck SR22 Load binds these to **E0**; deck keys may use sort or `refresh` instead)
- Commands: `list_sort_toggle_key`, `list_sort_toggle_direction` — toggle the browser sort key/direction
- Commands: `list_sort_filename`, `list_sort_timestamp`, `list_sort_asc`, `list_sort_desc` — explicit setters if you want fixed-state actions

**Legacy single-selection datarefs** (reflect the tapped/selected plan, not the visible page):

- `plan_name`, `plan_filename`, `plan_departure`, `plan_destination`
- `plan_distance_nm`, `plan_waypoint_count`
- `plan_dep_runway`, `plan_dest_runway`, `plan_sid`, `plan_star`
- `index`, `count`, `status`
- `loaded_distance_nm` — total distance of loaded route (nm)
- Commands: `previous`, `next` — move selection within the **current visible 3-row page only** (no page change); `load`, `refresh`

### fms_browser (live FMS)
- `fms_active_ident`, `fms_active_index`, `fms_active_altitude`
- `fms_first_ident`, `fms_last_ident`
- `fms_entry_count`

### fms_legs (FPL waypoint list)
- `row_1_index`, `row_1_ident`, `row_1_alt`, `row_1_is_active`, `row_1_is_selected`, `row_1_status`
- (same for row_2, row_3)
- `selected_index`, `entry_count`, `window_start` (read=page 1,2,3…; writable=set page)
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
