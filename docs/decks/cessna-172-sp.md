# Cessna 172 SP

## Supported Functions

<div class="grid cards" markdown>

-   :material-clock-fast:{ .lg .middle } __Primary Instruments__

    ---

    - [x] Airspeed Indicator
    - [ ] Attitude Indicator
    - [x] Heading Indicator
    - [ ] Turn Coordinator
    - [x] Altimeter
    - [x] Vertical Speed Indicator
  
-   :fontawesome-brands-markdown:{ .lg .middle } __Secondary Instruments__

    ---

    - [ ] Chronometer
    - [x] Fuel
    - [x] Exhaust Gas Temp / Fuel Flow
    - [x] Oil Temperature / Pressure
    - [x] Vac Pressure / Battery Ammeter
    - [x] Propeller RPM / Hobbs Meter
    - [ ] VOR1 / ILS Receiver
    - [ ] VOR2 Receiver
    - [ ] ADF Receiver


-   :material-format-font:{ .lg .middle } __Avionics__

    ---

    - [ ] Audio Switching Panel
    - [ ] GNS 530
    - [ ] GNS 430
    - [x] Transponder Panel
    - [x] Autopilot Panel
    - [ ] ADF Panel
    - [x] NAV / GPS Button

-   :material-scale-balance:{ .lg .middle } __Switch Panel__

    ---

    - [x] Magneto-Select, and Starter
    - [x] Master Alternator and Battery Switch
    - [x] Toggle Switches
    - [x] Avionics Bus Switches
    - [ ] Panel and Radio Brightness Controls
    - [ ] Pedestal and Glare-Shield Brightness Controls

-   :material-scale-balance:{ .lg .middle } __Throttle & Mixture / Pedestal__

    ---

    - [x] Throttle Lever
    - [x] Mixture Lever
    - [ ] Elevator Trim
    - [ ] Fuel Selector
    - [ ] Panel and Radio Brightness Controls
    - [ ] Pedestal and Glare-Shield Brightness Controls

-   :material-scale-balance:{ .lg .middle } __Annunciator Panel__

    ---

    - [x] L FUEL R
    - [x] OIL PRESS
    - [x] L VAC R
    - [x] VOLTS

</div>

## Specifications

=== "Engine"
    - **Model**: 1 x Lycoming IO-360-L2A (piston)
    - **Power**: 180 horsepower @ 2,700 rpm
    - **Propeller**: McCauley, 2-Bladed Fixed Pitch

=== "Fuel"
    - **Capacity**: 53 Gallons / 318 Lbs.
    - **Recommended fuel**: 100 Octane Low Lead (100LL)
    - **Fuel Burn (average)**: 8 Gallons per hour / 30 Liters per hour

=== "Weights and Capacities"
    - **Max. Takeoff Weight**: 2,550 lb. (1,157 kg)
    - **Max. Landing Weight**: 2,550 lb. (1,157 kg)
    - **Basic Empty Weight**: 1,640 lb. (744 kg)
    - **Max. Gross Weight**: 2,558 lb. (1088 kg)
    - **Max. Useful Load**: 918 lb. (416 kg)
    - **Maximum Payload**: 910 lb. (413 kg)

=== "Performance"
    - **Cruise Speed**: 124 KIAS
    - **Stall Speed (Clean)**: 48 KIAS
    - **Stall Speed (Landing Configuration)**: 40 KIAS
    - **Best Climb Rate**: 730 ft. pm (223 m. pm)
    - **Maximum Structural Speed**: 129 KIAS
    - **Landing Distance**: 1,335 ft. (407 m)
    - **Service Ceiling**: 14,000 ft. (4,267 m)
    - **Takeoff Distance**: 1,630 ft. (497 m)


## Supported Variants 

!!! note inline end "G1000"
    Additional buttons were added to support the additional G1000 AP functions (FD/VNAV/FLC).# Engine


- [x] Cessna_172SP_G1000
- [x] Cessna_172SP_seaplane
- [x] Cessna_172SP


## Pages

Deck consists of 7 pages which can be accessed via the lower hardware numbered button.



=== "PFI"
    PFI (Primary flight instruments)

    ![PFI](../assets/images/pfi.png)

    1. Altimeter includes barometer settings.
    2. Fuel quantity is displayed for both left and right tank.
    3. Oil button provides both temperature and pressure.
    4. Battery Ammeter is useful to see if batter is charging or depleting (noted if negative value).
    5. Caution annunciators provide oil pressure and voltage alarms.
    6. Warning annunciators provide fuel pressure and vacuum pressure alarms.
    7. NAVGPS displays NAV mode and provides toggle between NAV (VLOC) and GPS.
    8. Next Waypoint provides ETA, desired track (bearing) and NM left to reach waypoint.

=== "Switches"
    Switches (Battery, alternator, lights etc)
    ![](../assets/images/switches.png)

    !!! Warning
        PythonPlugin required for long press button (<X-Plane Path>/Resources/Plugins/PythonPlugins/PI_cockpitdecks_helper.py)

    - **Starter motor:** Long press push button functionality is facilitated by a Python plugin.
    - **Alternator:** Controls power supply to systems and battery charging when the engine is running.
    - **Battery:** Controls power supply when the engine is not running.
    - **Fuel Pump:** Controls electric fuel pump for priming engine and as a backup for mechanical pump failure.
    - **Beacon:** On/off control for rotating beacon light.
    - **Landing Lights:** On/off control for landing light.
    - **Taxi Lights:** On/off control for taxi light.
    - **Navigation Lights:** On/off control for wing and tail lights.
    - **Strobe Lights:** On/off control for wing strobe lights.
    - **Pitot Heat:** On/off control for pitot tube heater.
    - **Avionics Bus 1:** Powers BUS1, including Comm Panel, G530 GPS, Transponder, Autopilot, and BUS2.
    - **Avionics Bus 2:** Powers BUS2, including G430 GPS, VOR2, and ADF.


=== "FCU"
    FCU (Provides autopilot functions)
    ![](../assets/images/fcu.png)

    !!! Note
          Some functions are not available on S-TEC 55 Autopilot (Cessna 172 G530 model).

    - **AP:** Engages or disengages the autopilot system.
    - **FD:** *Not available on S-TEC 55 Autopilot model.* Provides visual cues for manual flight control based on autopilot logic without actually controlling the aircraft.
    - **HDG:** Heading mode. Autopilot turns the aircraft to heading selected via Heading Bug knob.
    - **ALT:** Altitude mode holds the current altitude.
    - **NAV:** Directs aircraft heading according to flight plan programmed into GPS (GPS mode) or to/from a radio navigation aid (VLOC mode).
    - **VNAV:** *Not available on S-TEC 55 Autopilot model.* Manages aircraft's vertical path according to a predefined route or waypoint altitudes.
    - **APR:** Activates an Instrument Landing System (ILS) approach mode for precision guidance during landing approaches.
    - **REV/BC:** Engages mode for flying an ILS localiser back-course approach, used for approaches where the aircraft is flying away from the beacon.
    - **VS:** Vertical speed mode to maintain an ascent or descent rate.
    - **FLC:** *Not available on S-TEC 55 Autopilot model.* Maintains a set airspeed while climbing or descending to a selected altitude.


=== "Radio"
    Radio (ADF, COM/NAV functions)
    ![](../assets/images/radio.png)

    - **ADF FREQ:** Displays ADF frequency and ADF standby frequency. Pressing button will swap frequencies.
    - **COM 1:** Displays COM1 frequency and COM1 standby frequency. Pressing button will swap frequencies.
    - **VLOC 1:** Displays NAV1 frequency and NAV1 standby frequency. Pressing button will swap frequencies.


=== "Engine"
    Engine (Displays engine data)
    ![](../assets/images/engine.png)

    - **ENG RPM:** Displays engine/prop RPM.
    - **MANIFOLD PRESSURE:** Displays manifold pressure.
    - **OIL TEMP:** Displays oil temperature.
    - **OIL PRESSURE:** Displays oil pressure.
    - **FUEL FLOW:** Display fuel flow in GPH.
      - Formula: `fuel_flow_kg_sec 3600 * 0.8 / 3.78541 / 2 roundn`
    - **CHT:** Displays cylinder head temp in celsius.
    - **BATTERY:**
      1. Displays battery charge in watts per hour.
      2. Displays battery amps (negative value means battery is discharging)
    - **THROTTLE:** Displays throttle as a percentage.
    - **FUEL EST:** Provides an estimate on fuel remaining in hours, based on current fuel flow.
      - Formula: `fuel_flow_kg_sec[0]} 3 roundn 0.000001 + / 3600 / 1 roundn`
    - **MIXTURE:** Displays fuel mixture as a percentage.

=== "Pedestal"
    Pedestal (Flaps, gear)
    ![](../assets/images/pedestal.png)

    - **THROTTLE:** Displays throttle as a percentage.
    - **TOGGLE BRAKES:** Displays the state of the parking brake. Push will toggle parking brake on/off.
    - **MIXTURE:** Displays fuel mixture as a percentage.
    - **FLAPS UP:** Extends flaps one notch.
    - **FLAPS RATIO:** Displays flaps state as a number between 0 and 1 (0 fully retracted, 1 fully extended).
    - **FLAPS DOWN:** Retracts flaps one notch.

=== "Transponder"
    Transponder (Change transponder mode and id)
    ![](../assets/images/transponder.png)

    - **SQUAWK CODE BUTTONS:** The top four buttons display the squawk code and serve as push buttons to increment the transponder digits.
    - **Transponder Mode Buttons:**
      1. ON
      2. OFF
      3. STBY
      4. ALT
      5. TEST
    - **IDENT:** Transmits radio beacon for a short period of time.
    - **RADIO BEACON:** Displays an R if the transponder is broadcasting. This will display intermittently or constantly for a short period of time if IDENT is pushed.
    - **MODE:** Displays the current mode of the transponder.


