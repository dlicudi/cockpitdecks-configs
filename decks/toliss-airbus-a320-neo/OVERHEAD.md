# A320neo Overhead Pages — Status & Notes

Covers the iPad layout (`deckconfig/ipad1/`) overhead panel pages.
The Stream Deck XL layout has one partial overhead page (`overhead_antiice.yaml`);
the overhead work described here is iPad-only.

---

## Architecture

The overhead is a hub-and-spoke design.

`overhead.yaml` is the entry point — a navigation hub with a few quick-access
controls (crew oxygen, cargo ventilation). Every sub-page includes
`overhead-pager.yaml`, which adds a persistent three-column sidebar
(columns 9–11) providing one-tap navigation to any system page. Index 96 on
every page is a HOME button back to the hub.

There are 22 sub-pages, one per A320 overhead system panel.

---

## Data Sources for AI Agents

When adding or fixing buttons, these are the most useful sources for correct
datarefs and expected values.

### DataRefTool last-run export (best offline source)

After any X-Plane session with the DataRefTool plugin active, every dataref
observed during that session is written to:

    <X-Plane Home>/Output/preferences/drt_last_run_datarefs.txt

This file lists each dataref with its type and last observed value. It is the
best starting point for AI agents — it can be read without X-Plane running and
reflects what the actual aircraft model exposes.

### ToLiss A320neo aircraft manual

The PDF manual shipped with the aircraft contains an appendix of all custom
`AirbusFBW/*` datarefs with index mappings. This is authoritative for what
each array element means.

### ToLiss forum (x-plane.org)

Community members frequently post confirmed dataref mappings and array indices,
especially for fault/warning lights. Search under the A320neo product forum.

### OHPLightsATA pattern

Fault light states follow a consistent pattern across systems:

    AirbusFBW/OHPLightsATA{chapter}[N]

For example, `overhead-probe-heat.yaml` uses `AirbusFBW/OHPLightsATA30[11]`
for the FAULT light. The same pattern applies to other ATA chapters:

- ATA 24 (Electrical) → `AirbusFBW/OHPLightsATA24[N]`
- ATA 28 (Fuel) → `AirbusFBW/OHPLightsATA28[N]`
- ATA 29 (Hydraulics) → `AirbusFBW/OHPLightsATA29[N]`
- ATA 34 (ADIRU) → `AirbusFBW/OHPLightsATA34[N]`
- ATA 36 (Pneumatics/Bleed) → `AirbusFBW/OHPLightsATA36[N]`

Array indices need runtime verification with DataRefTool.

---

## Page-by-Page Status

Items marked `[fault light stubbed]` have working switch activation but their
FAULT annunciator part uses `formula: 0` (always off) because the correct
dataref index has not yet been confirmed.

---

### overhead-adiru — ADIRU / IR / ADR

Mode selectors and alignment controls for the three inertial reference units.

- ADIRS ON BAT — display only, shows if ADIRS powered on battery
- ADIRU FAST ALIGN — pushbutton to trigger fast alignment mode
- IR 1 ALIGN — IR1 alignment status annunciator
- IR 3 ALIGN — IR3 alignment status annunciator
- IR 2 ALIGN — IR2 alignment status annunciator
- IR 1 — circular switch, IR mode selector (OFF / NAV / ATT)
- IR 3 — circular switch, IR3 mode selector
- IR 2 — circular switch, IR2 mode selector
- ADR 1 — ADR 1 OFF pushbutton `[fault light stubbed]`
- ADR 3 — ADR 3 OFF pushbutton `[fault light stubbed]`
- ADR 2 — ADR 2 OFF pushbutton `[fault light stubbed]`

---

### overhead-aice-eng — Anti-Ice (Engine & Wing)

Wing and engine anti-ice switches plus engine mode selector and master switches.
Grouped here because these panels sit adjacent on the real overhead.

- WING A/ICE — wing anti-ice pushbutton with FAULT/ON display
- ENG 1 A/ICE — engine 1 anti-ice pushbutton with FAULT/ON display
- ENG 2 A/ICE — engine 2 anti-ice pushbutton with FAULT/ON display
- PRB/WIN HT — probe and window heat pushbutton (links to probe-heat page)
- ENG MODE — engine mode selector switch (CRANK / NORM / IGN START)
- ENG MASTER 1 — engine 1 master switch with ON display
- ENG MASTER 2 — engine 2 master switch with ON display
- MAN START 1 — engine 1 manual start with FAULT/ON display

---

### overhead-apu — APU

APU master, start, and bleed switches plus EGT and N% readouts.

- APU MASTER — APU master pushbutton with FAULT/AVAIL display
- APU START — APU start pushbutton with ON/AVAIL display
- APU BLEED — APU bleed air pushbutton with FAULT/ON display
- APU EGT — display-only text readout of APU exhaust gas temperature
- APU N% — display-only text readout of APU spool speed

---

### overhead-bleed-packs-press — Bleed Air / Packs / Pressurization

Engine bleed switches, cross-bleed selector, pack controls, hot air, ram air,
and cabin pressurization mode and readouts.

- ENG1 BLD — engine 1 bleed pushbutton `[fault light stubbed]`
- X BLEED indicator — display-only cross-bleed valve position
- ENG2 BLD — engine 2 bleed pushbutton `[fault light stubbed]`
- HP BLD 1 — HP bleed 1 display (status indicator)
- HP BLD 2 — HP bleed 2 display (status indicator)
- X BLEED selector — rotary cross-bleed valve selector (SHUT / AUTO / OPEN)
- PACK 1 — pack 1 pushbutton with FAULT/OFF display `[fault light stubbed]`
- PACK FLOW — pack flow selector (LO / NORM / HI)
- PACK 2 — pack 2 pushbutton with FAULT/OFF display
- HOT AIR — hot air pushbutton with FAULT/OFF display
- RAM AIR — ram air pushbutton with ON display
- MODE SEL — cabin pressurisation mode selector (MAN / AUTO)
- LDG ELEV — landing elevation display/selector
- CAB ALT — cabin altitude readout
- DELTA P — differential pressure readout
- CAB V/S — cabin vertical speed readout
- OFV POS — outflow valve position readout

---

### overhead-calls — Cabin Calls

Crew call pushbuttons for mechanic, forward cabin, aft cabin, and emergency.

- MECH — mechanic call pushbutton with ON display
- FWD — forward cabin call pushbutton with pink call light display
- AFT — aft cabin call pushbutton with pink call light display
- EMER — emergency call pushbutton with ON display

---

### overhead-cargo-smoke — Cargo Ventilation & Smoke

Cargo compartment ventilation switches and smoke detection status displays.

- CARGO FWD — forward cargo ventilation switch with ON/OFF display
- CARGO AFT — aft cargo ventilation switch with ON/OFF display
- FWD SMOKE — forward cargo smoke detector status (display only)
- AFT SMOKE — aft cargo smoke detector status (display only)

---

### overhead-elec — Electrical

Generators, bus tie, AC essential feed, IDG disconnect, batteries and readouts.

- GEN 1 — generator 1 pushbutton with FAULT/OFF display `[fault light stubbed]`
- APU GEN — APU generator status display (display only)
- GEN 2 — generator 2 pushbutton with FAULT/OFF display `[fault light stubbed]`
- EXT PWR — external power pushbutton with AVAIL/ON display
- BUS TIE — bus tie status display (display only)
- AC ESS FEED — AC essential feed status display (display only)
- GALLEY — galley power status display (display only)
- IDG 1 — IDG 1 disconnect pushbutton with FAULT/DISC display `[fault light stubbed]`
- IDG 2 — IDG 2 disconnect pushbutton with FAULT/DISC display `[fault light stubbed]`
- BAT 1 — battery 1 pushbutton with FAULT/OFF display
- BAT 2 — battery 2 pushbutton with FAULT/OFF display
- BAT 1A — battery 1 amperage readout (display only)
- BAT 2A — battery 2 amperage readout (display only)
- BAT 1V — battery 1 voltage readout (display only)
- BAT 2V — battery 2 voltage readout (display only)

---

### overhead-emer-elec — Emergency Electrical

Emergency generator test, GEN 1 line, RAT deployment, and manual on.

- EMER GEN TEST — emergency generator test switch
- GEN 1 LINE — generator 1 line contactor switch with FAULT/OFF display
- RAT & EMER GEN — RAT manual deployment pushbutton with FAULT/ON display
- MAN ON — emergency electrical manual on pushbutton

---

### overhead-eng-start — Engine Start

Engine mode selector and manual start switches with cover guards.

- ENG MODE — engine mode selector switch (CRANK / NORM / IGN START)
- MODE — engine mode status annunciator (display only)
- ENG1 MAN START — engine 1 manual start switch (guarded) with FAULT display
- ENG1 START — engine 1 start light status annunciator (display only)
- ENG2 MAN START — engine 2 manual start switch (guarded) with FAULT display
- ENG2 START — engine 2 start light status annunciator (display only)

---

### overhead-evac — Evacuation

Evacuation command switch, horn shutoff, and mode selector.

- COMMAND — evacuation command switch (guarded) with ON display
- HORN SHUT OFF — evacuation horn shutoff pushbutton
- CAPT & PURS — evacuation mode selector (CAPT ONLY / CAPT & PURS)

---

### overhead-extlt — External Lights

All external lighting switches.

- STROBE — strobe light selector (OFF / AUTO / ON)
- BEACON — beacon light switch with ON display
- WING — wing/engine scan light switch with ON display
- NAV & LOGO — navigation and logo light selector (OFF / NAV / NAV & LOGO)
- NOSE/TAXI — nose and taxi light selector (OFF / T.O. / TAXI)
- RWY TURN OFF — runway turnoff lights switch with ON display
- LAND L — left landing light switch (RETRACT / OFF / ON)
- LAND R — right landing light switch (RETRACT / OFF / ON)

---

### overhead-fire — Fire Detection & Extinguishing

Engine and APU fire handles, test pushbuttons, and extinguisher agent buttons.

- ENG 1 fire handle — display only, shows FIRE/ARMED state
- ENG1 TEST — fire system test pushbutton
- ENG1 AGT 1 — engine 1 extinguisher agent 1 button with SQUIB/DISCH display
- ENG1 AGT 2 — engine 1 extinguisher agent 2 button with SQUIB/DISCH display
- APU fire handle — display only, shows FIRE/ARMED state
- APU TEST — APU fire system test pushbutton
- APU AGT — APU extinguisher agent button with SQUIB/DISCH display
- ENG 2 fire handle — display only, shows FIRE/ARMED state
- ENG2 TEST — fire system test pushbutton
- ENG2 AGT 1 — engine 2 extinguisher agent 1 button with SQUIB/DISCH display
- ENG2 AGT 2 — engine 2 extinguisher agent 2 button with SQUIB/DISCH display

---

### overhead-fltctl — Flight Controls

ELAC, SEC, and FAC computer pushbuttons.

- ELAC 1 — ELAC 1 pushbutton with FAULT/OFF display
- SEC 1 — SEC 1 pushbutton with FAULT/OFF display
- FAC 1 — FAC 1 pushbutton with FAULT/OFF display
- SEC 2 — SEC 2 pushbutton with FAULT/OFF display
- SEC 3 — SEC 3 pushbutton with FAULT/OFF display
- ELAC 2 — ELAC 2 pushbutton with FAULT/OFF display
- FAC 2 — FAC 2 pushbutton with FAULT/OFF display

---

### overhead-fuel — Fuel

Wing and centre tank pump switches, mode selector, cross-feed valve, and quantity readout.

- FUEL L1 — left wing pump 1 switch with FAULT/OFF display `[fault light stubbed]`
- FUEL L2 — left wing pump 2 switch with FAULT/OFF display `[fault light stubbed]`
- CTR L XFR — centre tank left transfer pump switch with FAULT/OFF display `[fault light stubbed]`
- CTR R XFR — centre tank right transfer pump switch with FAULT/OFF display `[fault light stubbed]`
- FUEL R1 — right wing pump 1 switch with FAULT/OFF display `[fault light stubbed]`
- FUEL R2 — right wing pump 2 switch with FAULT/OFF display `[fault light stubbed]`
- MODE SEL — fuel mode selector switch with FAULT/AUTO display `[fault light stubbed]`
- X FEED — cross-feed valve switch with OPEN/SHUT display

---

### overhead-gpws — GPWS / EGPWS

Ground proximity warning system inhibit switches.

- TERR — terrain display inhibit pushbutton with OFF display
- SYS — GPWS system inhibit pushbutton with OFF display
- G/S MODE — glideslope mode inhibit pushbutton with OFF display
- FLAP MODE — flap mode inhibit pushbutton with OFF display
- LDG FLAP 3 — landing flap 3 inhibit pushbutton with OFF display

---

### overhead-hyd — Hydraulics

Engine-driven, electric, and PTU hydraulic pump switches plus RAT manual deployment.

- HYD ENG1 — engine 1 hydraulic pump switch with FAULT/OFF display `[fault light stubbed]`
- ELEC BLUE — blue electric hydraulic pump switch with FAULT/OFF display `[fault light stubbed]`
- PTU — power transfer unit switch with FAULT/OFF display `[fault light stubbed]`
- RAT MAN ON — RAT manual on pushbutton (guarded) with ON display
- HYD ENG2 — engine 2 hydraulic pump switch with FAULT/OFF display `[fault light stubbed]`
- ELEC YLW — yellow electric hydraulic pump switch with FAULT/OFF display `[fault light stubbed]`

---

### overhead-intlt — Internal Lights

Dome light, annunciator light mode, standby compass light.

- DOME — dome light selector (OFF / DIM / BRT)
- ANN LT — annunciator light mode switch (TEST / BRT / DIM)
- STBY COMPASS — standby compass light switch
- COMPASS LT — compass light intensity control

---

### overhead-oxygen — Oxygen

Crew and passenger oxygen controls.

- MASK MAN ON — oxygen mask manual on pushbutton with ON display
- PASSENGER — passenger oxygen status display (display only)
- CREW SUPPLY — crew oxygen supply switch with OFF display

---

### overhead-probe-heat — Probe / Window Heat

Single pushbutton controlling probe and window heat with FAULT and AUTO/ON display.

- PROBE/WINDOW HEAT — probe heat switch with FAULT/ON display (uses `AirbusFBW/OHPLightsATA30[11]` for FAULT — this is the reference implementation for other FAULT lights)
- HEAT STATUS — auto/on status display derived from switch position (display only)

---

### overhead-rcdr — Recorders

CVR ground control, erase, and test.

- GND CTL — recorder ground control switch with ON display
- CVR ERASE — CVR erase pushbutton with ON display
- CVR TEST — CVR test pushbutton with ON display

---

### overhead-signs — Cabin Signs & Wipers

Cabin signs, emergency exit lights, ditching switch, and wiper controls.

- SEAT BELTS — seat belt sign selector (OFF / AUTO / ON)
- NO SMOKE — no smoking sign selector (OFF / AUTO / ON)
- EMER EXIT — emergency exit light switch (ARM / OFF / ON)
- DITCHING — ditching switch (guarded) with ON display
- Wipers (left) — left windshield wiper selector (PARK / INTMT / LOW / HIGH)
- Wipers R (right) — right windshield wiper selector
- RAIN RPLNT — rain repellent pushbutton with ON display

---

### overhead-ventilation — Ventilation

Blower, extract, and cabin fan switches with status annunciators.

- BLOWER — blower switch (OVRD / NORM)
- BLOWER status — blower override status annunciator (display only)
- EXTRACT — extract switch (OVRD / NORM)
- EXTRACT status — extract override status annunciator (display only)
- CAB FANS — cabin fans switch with OFF display
- FANS STATUS — cabin fans status annunciator (display only)

---

## Summary

All 22 pages have been implemented. The remaining work is verifying or
discovering correct dataref indices for FAULT lights on 5 pages.

### VERIFY — formula is plausible but index not confirmed in-sim

These have been replaced from `formula: 0` with a real dataref. The dataref
name is confirmed in the DRT export but the array index is inferred by
analogy and needs sim-side verification with DataRefTool.

- overhead-fuel: FUEL L1 FAULT = `FuelTVSDArray[0]` (confirmed from A321 reference)
- overhead-fuel: FUEL L2, CTR L, CTR R, R1, R2, MODE SEL FAULT = `FuelTVSDArray[1..6]` (assumed)
- overhead-hyd: HYD ENG1, ELEC BLUE, PTU, HYD ENG2 FAULT = `HydPumpOHPArray[0,2,4,1]` (assumed)
- overhead-elec: APU GEN FAULT = `OHPLightsATA49[0]` (ATA49 confirmed in DRT, index 0 guessed)

### TODO — no known dataref found anywhere

These remain `formula: 0`. The same stubs exist in A321/A330 reference configs,
so this is not a gap unique to this A320 config. Needs in-sim investigation.

- overhead-adiru: ADR 1/2/3 FAULT — `OHPLightsATA34` is in DRT but which indices map to ADR fault is unknown; IR ALIGN uses indices [6],[8],[10]
- overhead-bleed-packs-press: ENG1/ENG2 BLEED FAULT — no `OHPLightsATA36` in DRT; `ENG1BleedInd`/`ENG2BleedInd` encoding unknown
- overhead-bleed-packs-press: HOT AIR FAULT — `HotAirSwitchIllum` and `HotAirValve` both in DRT; possible: `${AirbusFBW/HotAirSwitchIllum} ${AirbusFBW/HotAirValve} - abs`
- overhead-elec: BUS TIE FAULT — not found in any reference config
- overhead-elec: BAT 1/2 FAULT — not found in any reference config; `OHPLightsATA24` higher indices possible
