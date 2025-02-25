# Home Assistant Integration for Silence Scooter
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)
![Version](https://img.shields.io/github/v/release/lorenzo-deluca/homeassistant-silence)
![Downloads](https://img.shields.io/github/downloads/lorenzo-deluca/homeassistant-silence/total)
[![](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86)](https://github.com/sponsors/lorenzo-deluca)
[![buy me a coffee](https://img.shields.io/badge/support-buymeacoffee-222222.svg?style=flat-square)](https://www.buymeacoffee.com/lorenzodeluca)

> Silence.eco Scooter data for [Home Assistant][https://www.home-assistant.io]

This is a Home Assistant custom component that integrate data from you Silence Scooter to Home Assistant.
If you like this project you can support me with :coffee: , with **GitHub Sponsor** or simply put a :star: to this repository :blush:

[![](https://img.shields.io/static/v1?label=Sponsor&message=%E2%9D%A4&logo=GitHub&color=%23fe8e86)](https://github.com/sponsors/lorenzo-deluca)
<a href="https://www.buymeacoffee.com/lorenzodeluca" target="_blank">
  <img src="https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png" alt="Buy Me A Coffee" width="150px">
</a>

# Disclaimer
This plugin was developed by analyzing traffic from official Silence Connected App, it was not sponsored or officially supported by Silence.eco
If someone from Silence would like to contribute or collaborate please contact me at [me@lorenzodeluca.dev](mailto:me@lorenzodeluca.dev?subject=[GitHub]homeassistance-Silence)

# 🚨 UPDATE JULY 2024
> **NEW PROJECT (Open Source Private Server):** 
With the help of other users and since the applications are becoming pay-as-you-go, we have created an alternative project whereby you can create your own private server, becoming completely autonomous and not sending any data to Silence/Seat.
This project should also work with Seat Mò scooters.
[Private Server](https://github.com/lorenzo-deluca/silence-private-server)

---

## Installation
You can install this plugin like any other hacs integration on home assistant.

### HACS
- Add repository "https://github.com/lorenzo-deluca/homeassistant-silence" to custom repositories and select "Integration" category.
- Click on "Install" in the plugin card.

### Manual
Copy or link [`silencescooter`](./custom_components/silencescooter) subfolder to `config/custom_components`.

## Configuration
Configure you Scooter with Silence APP, edit `configuration.yaml` file adding this sensor with your app credentials.

```YAML
sensor:
  - platform: silencescooter
    name: MySilenceScooter
    username: !secret silenceuser
    password: !secret silencepassword
```

# Home Assistant
After installing and configuring the plugin you will be able to view on home assistant all the data of your scooter silence, 
keep statistics and use them for your automations.

## Entities
After installation and configuration, if everything is working (if not, check the registry by searching 'silence'), 
you will find several sensor entities named 'silence.xxx' 

<img alt="HA Entities" src="images/ha-entities.png" width="650">
<img alt="HA Battery Soc" src="images/ha-batterysoc.png" width="650">

## Lovelace
You can create various tabs like this one

![Lovelace Scooter](images/ha-scooter.png)

Here is the YAML code, you need some HACS Frontend integration installed: 
- [x] `vertical-stack-in-card`
- [x] `custom:mini-graph-card`

```YAML
type: custom:vertical-stack-in-card
cards:
  - type: picture
    image: local/dark_logo.png
  - type: custom:bar-card
    height: 35px
    entities:
      - entity: sensor.silence_batterysoc
        name: Battery SoC
  - type: entities
    entities:
      - entity: sensor.silence_status
        name: Status
      - entity: sensor.silence_alarmactivated
        name: Alarm
      - entity: sensor.silence_batteryout
        name: Battery Out
      - entity: sensor.silence_charging
        name: In Charging
      - entity: sensor.silence_odometer
        name: Odometer
      - entity: sensor.silence_range
        name: Range
      - entity: sensor.silence_velocity
        name: Speed
      - entity: sensor.silence_lastreporttime
        name: Last Update
  - type: glance
    title: Scooter
    entities:
      - entity: sensor.silence_name
        name: Name
      - entity: sensor.silence_color
        name: Color
      - entity: sensor.silence_model
        name: Model
      - entity: sensor.silence_manufacturedate
        name: Manufacture
      - entity: sensor.silence_frameno
        name: Frame
      - entity: sensor.silence_imei
        name: IMEI
    show_icon: false
  - type: horizontal-stack
    title: Temperature
    cards:
      - type: custom:mini-graph-card
        entities:
          - entity: sensor.silence_motortemperature
            name: Motor
            line_color: red
      - type: custom:mini-graph-card
        entities:
          - entity: sensor.silence_invertertemperature
            name: Inverter
      - type: custom:mini-graph-card
        entities:
          - entity: sensor.silence_batterytemperature
            name: Battery
```

## Device Tracker
For device tracking you can use this automation to update a dummy device tracker called `silence_scooter_tracker`

```YAML
alias: Auto - Silence Scooter Update Location
description: ""
trigger:
  - platform: state
    entity_id:
      - sensor.silence_location_latitude
  - platform: state
    entity_id:
      - sensor.silence_location_longitude
  - platform: homeassistant
    event: start
condition: []
action:
  - service: device_tracker.see
    data:
      dev_id: silence_scooter_tracker
      gps:
        - "{{ states('sensor.silence_location_latitude') }}"
        - "{{ states('sensor.silence_location_longitude') }}"
mode: single
```

![HA Device Tracker](images/ha-tracking.png)

# Work in Progress
Remote controls from the app, such as on/off, opening the under seat and alarm activation, are still to be managed.
I have captured the apis but I still have to implement the services from Home Assistant.
Any help is welcome, if you have new implementations feel free to make pull requests :blush:

## Tested on Silence Scooters
- [x] Silence S01 Connected
- [x] Silence S01+

## Known issues (FAQ)
- For now desn't work with Seat Mo [https://github.com/lorenzo-deluca/homeassistant-silence/issues/3] because Seat use different cloud provider.

# License
GNU AGPLv3 © [Lorenzo De Luca][https://lorenzodeluca.dev]
