# Home Assistant Integration for Silence Scooter
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)
![Version](https://img.shields.io/github/v/release/lorenzo-deluca/homeassistant-silence)
![Downloads](https://img.shields.io/github/downloads/lorenzo-deluca/homeassistant-silence/total)

This is a Home Assistant custom component (sensor) that integrate data from you Silence S01 Scooter to Home Assistant

[![buy me a coffee](https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png)](https://www.buymeacoffee.com/lorenzodeluca)

The sensor will check every hour if a new reading can be retrieved but Greenchoice practically only gives us one reading a day over this API. The reading is also delayed by 1 or 2 days (this seems to vary). The sensor will give you the date of the reading as an attribute.

### Install:
1. Search for 'silence-scooter' in [HACS](https://hacs.xyz/). 
    *OR*
   Place the 'silence-scooter' folder in your 'custom_compontents' directory if it exists or create a new one under your config directory.
2. Add the component to your configuration.yaml, an example of a proper config entry:

```YAML
sensor:
  - platform: silence-scooter
    name: MySilenceScooter
    username: !secret silenceuser
    password: !secret silencepassword
```