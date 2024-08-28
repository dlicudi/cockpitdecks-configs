# cockpitdecks-configs
A collection of aircraft configs for [cockpitdecks](https://github.com/devleaks/cockpitdecks).

~~Important: New config currently requires this experimental build of [cockpitdecks](https://github.com/dlicudi/cockpitdecks).~~

Documentation: [Cockpitdecks Configs Docs](http://dlicudi.github.io/cockpitdecks-configs/)

## Aircraft

Aircraft configs completed, planned or in progress.

### Laminar Research
- [x] LR Cessna 172 SP (Laminar Research)
- [x] LR Cirrus SR22 (Laminar Research) 
- [x] LR Beechcraft Baron 58 (Laminar Research)
- [x] LR Lancair Evolution (Laminar Research)

### Toliss
- [x] Toliss Airbus A321 Neo (devleaks)
- [ ] Toliss Airbus A320 Neo

### Aerobask
- [ ] LR Robin DR401 (Aerobask)


## Examples

### Home
![Home](./docs/assets/images/cirrus-sr22/home.png)

### Primary Flight Instruments
![PFI](./docs/assets/images/cirrus-sr22/pfi.png)

### Garmin GCU-478
![GCU-478](./docs/assets/images/cirrus-sr22/gcu478.png)


## Notes on long press buttons and helper plugin

> [!IMPORTANT]
> The helper plugin must be copied to PythonScripts e.g.
> `cp ~/Documents/GitHub/cockpitdecks/PI_cockpitdecks_helper.py ~/X-Plane\ 12/Resources/plugins/PythonPlugins/`
>
> You must have either the deckconfig in the Aircraft's folder or a symlink (on MAC an alias will not work) e.g.
> `ln -s ~/Documents/GitHub/cockpitdecks-configs/decks/cessna-172-sp/deckconfig ~/X-Plane\ 12/Aircraft/Laminar\ Research/Cessna\ 172\ SP`

## Issues
- ~~Possible issues with helper plugin not working for multiple long press buttons~~