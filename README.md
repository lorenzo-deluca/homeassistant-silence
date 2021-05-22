# Home Assistant Integration for Silence Scooter
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)
![Version](https://img.shields.io/github/v/release/lorenzo-deluca/homeassistant-silence)
![Downloads](https://img.shields.io/github/downloads/lorenzo-deluca/homeassistant-silence/total)

This is a Home Assistant custom component (sensor) that integrate data from you Silence S01 Scooter to Home Assistant

[![buy me a coffee](https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png)](https://www.buymeacoffee.com/lorenzodeluca)

# Disclaimer
This plugin was developed by analyzing traffic from official Silence app, it was not sponsored by Silence.eco
If someone from Silence would like to share it please contact me at [me@lorenzodeluca.dev](mailto:me@lorenzodeluca.dev?subject=[GitHub]Ha-Silence)

## Home Assistant
After installing and configuring the plugin you will be able to view on home assistant all the data of your scooter silence, 
keep statistics and use them for your automations.

![HA Entities](https://raw.githubusercontent.com/lorenzo-deluca/homeassistant-silence/master/images/ha-entities.png)
![HA Battery Soc](https://raw.githubusercontent.com/lorenzo-deluca/homeassistant-silence/master/images/ha-batterysoc.png)

### Installation
You can install this plugin like any other hacs integration on home assistant.

#### HACS
- Add repository "https://github.com/lorenzo-deluca/homeassistant-silence" to custom repositories and select "Integration" category.
- Click on "Install" in the plugin card.

#### Manual
Copy or link [`silence-scooter`](./custom_components/silence-scooter) subfolder to `config/custom_components`.

### Configuration
Configure you Scooter with Silence APP, edit `configuration.yaml` file adding this sensor with your app credentials.


```YAML
sensor:
  - platform: silencescooter
    name: MySilenceScooter
    username: !secret silenceuser
    password: !secret silencepassword
```

## Work in Progress
The plugin is still under development, the `device_tracker` entity with the scooter positioning will be implemented as well.
If you have new implementations feel free to make pull requests :) 