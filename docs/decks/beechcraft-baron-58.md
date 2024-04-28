---
icon: material/airplane
---

# Beechcraft Baron 58

## Cockpit Functions

This section covers cockpit functions for the Beechcraft Baron 58. In bold are functions which are currently supported by this deck.

### Primary Instruments
:small_blue_diamond:
**Airspeed Indicator**
:small_blue_diamond:
Attitude Indicator (AI)
:small_blue_diamond:
Horizontal Situation Indicator (HSI)
:small_blue_diamond:
Turn Coordinator
:small_blue_diamond:
**Altimeter**
:small_blue_diamond:
Distance Measuring Equipment (DME) Master Display
:small_blue_diamond:
**Vacuum Gauge**
:small_blue_diamond:
ADF (Automatic Direction Finder)
:small_blue_diamond:
**Variometer**
:small_blue_diamond:
VOR / ILS Receiver
:small_blue_diamond:

### Engine Instrumentation
:small_blue_diamond:
**Manifold Pressure**
:small_blue_diamond:
**Propeller RPM**
:small_blue_diamond:
**Fuel Flow**
:small_blue_diamond:
**Engine Temperature**
:small_blue_diamond:
**Oil Temperature and Pressure**
:small_blue_diamond:

### Avionics Panel
:small_blue_diamond:
Audio Switching Panel
:small_blue_diamond:
**Transponder**
:small_blue_diamond:
**COMM 1 and COMM 2 Radios**
:small_blue_diamond:
**NAV 1 and NAV 2 Radios**
:small_blue_diamond:
GNS 530
:small_blue_diamond:
**ADF Frequency Selection Panel**
:small_blue_diamond:

### Instrument Sub Panel
:small_blue_diamond:
**Master Electrical Switches**
:small_blue_diamond:
**Avionics Master Power and Prop Sync**
:small_blue_diamond:
**Pitot Heat Switches**
:small_blue_diamond:
**Icing Switches**
:small_blue_diamond:
**Fuel Boost Pump Switches**
:small_blue_diamond:
**Lights Panel**
:small_blue_diamond:
Landing Gear Lever
:small_blue_diamond:
**Parking Brake**
:small_blue_diamond:
**Fuel Gauges**
:small_blue_diamond:
Prop Amps and De-Icing Gauges
:small_blue_diamond:
Flap Lever
:small_blue_diamond:
Panel Light Dimmers
:small_blue_diamond:

### Throttle Quadrant and Center Console
:small_blue_diamond:
**Throttle Levers**
:small_blue_diamond:
Prop Levers
:small_blue_diamond:
**Mixture Levers**
:small_blue_diamond:
Rudder Trim Wheel
:small_blue_diamond:
Elevator Trim Wheel
:small_blue_diamond:
Aileron Trim Wheel
:small_blue_diamond:
Cowl Flap Levers
:small_blue_diamond:

### Autopilot
:small_blue_diamond:
**AP ON/OFF**
:small_blue_diamond:
**HDG (Heading) Mode**
:small_blue_diamond:
**FD ON**
:small_blue_diamond:
**ALT (Altitude) Mode**
:small_blue_diamond:
**NAV (Navigation) Mode**
:small_blue_diamond:
**BC (Back Course) Mode**
:small_blue_diamond:
**APPR Mode**
:small_blue_diamond:
YAW ON
:small_blue_diamond:
**DN / UP Rocker Switch**
:small_blue_diamond:

## Deck Functions

This section provides details on this deck and its pages, buttons and encoders.

### Encoders

#### FCU

Provides barometer setting (QNH), throttle/mix (**THR**/**MIX**) controls and autopilot controls such as **HDG** and **VS**. 

#### Pedestal
In progress.

#### Radio

These encoders are not working currently.
- [ ] XPDR (not currently functioning)
- [ ] MODE (Changes transponder mode)
- [ ] ADF (not currently functioning)
- [ ] COM (not currently functioning)
- [ ] VLOC (not currently functioning)

### Pages

#### Home
![](../assets/images/beechcraft-baron-58/home.png){ :width="200" }

The home page provides an index to all the various pages available (up to a total of 12).

The bottom buttons can provide quick access to up to 7 different pages.


!!! note warning
    Various pages are still work in progress (e.g. Pedestal, Views)

    GCU-478 will be replaced with another page.


#### PFI
![](../assets/images/beechcraft-baron-58/pfi.png){ :width="200" }

Central to this page is data you would consider primary flight instruments.
The **speed**, **bearing**, **altitude** and **vertical speed** fill the first row.

The second row consists of engine data in a more compact form than that found in the engine page.

The third row consists of:

- Fuel duration (a calculation of time remaining based on fuel flow and fuel quantity).
- Caution annunciators.
- Warning annunciators.
- Information on the next waypoint in flight plan.

#### Switches
![](../assets/images/beechcraft-baron-58/switches.png){ :width="200" }

This page provides buttons for **battery**, **alternators**, **avionics**, **prop sync** and **fuel pumps**.

There are also two ignition buttons **IGN 1** and **IGN 2** which are longpress buttons to start engines.

**Icing** and **lights** have had to be placed in separate pages as it was impossible to fit them here.


#### Icing
![](../assets/images/beechcraft-baron-58/icing.png){ :width="200" }

There are buttons to cover icing functions for left and right pitot (**PITOT L** and **PITOT R**), stall warn, prop and windshield.

For boots functions there is a **BOOTS AUTO** which can set the boots to inflate automatically at intervals, a button to switch boots off (**BOOTS OFF**) and a longpress button (**BOOTS**) that can be used to manually inflate boots.



#### Lights
![](../assets/images/beechcraft-baron-58/lights.png){ :width="200" }

Most of these are self explanatory. One possible improvement will be to add encoders for the panel lights.  

#### FCU
![](../assets/images/beechcraft-baron-58/fcu.png){ :width="200" }

#### Radio
![](../assets/images/beechcraft-baron-58/radio.png){ :width="200" }

#### Engine
![](../assets/images/beechcraft-baron-58/engine.png){ :width="200" }

#### Pedestal
![](../assets/images/beechcraft-baron-58/pedestal.png){ :width="200" }

#### Transponder
![](../assets/images/beechcraft-baron-58/transponder.png){ :width="200" }

#### Weather
![](../assets/images/beechcraft-baron-58/weather.png){ :width="200" }

This page provides comprehensive weather data including coverage for different cloud layers and tropo data.

----

## Procedures
Procedures in relation to Loupedeck functions.


### Before Starting Engines
- [ ] Exterior Inspection – COMPLETED
- [x] Parking Brake – ON
- [x] Power Levers – SLIGHTLY FORWARD
- [ ] Propeller Levers – FULL FORWARD
- [x] Mixture Levers – FULL FORWARD
- [x] All switches – OFF
- [x] Battery Switch – ON
- [x] Fuel Quantity – CHECK
- [ ] Check Annunciator Panel Warning Lights.

### Engine Start 

- [x] Master Battery Switch – CHECK ON
- [x] Avionics Master Switch – OFF
- [ ] Left Alternator Switch – ON
- [x] Left Magneto Switch – START (hold until engine running)

#### When Left Engine Running
- [x] Left Power Lever – IDLE (FULL BACK)
- [ ] Left Magneto Switch – CHECK BOTH
- [ ] Right Alternator Switch – ON
- [x] Right Magneto Switch – START (hold until engine running)

#### When Right Engine Running
- [x] Right Power Lever – IDLE (FULL BACK)
- [x] Right Magneto Switch – CHECK BOTH
