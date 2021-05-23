# Home Assistant Integration for Silence Scooter
[![hacs_badge](https://img.shields.io/badge/HACS-Default-orange.svg)](https://github.com/custom-components/hacs)
![Version](https://img.shields.io/github/v/release/lorenzo-deluca/homeassistant-silence)
![Downloads](https://img.shields.io/github/downloads/lorenzo-deluca/homeassistant-silence/total)
[![buy me a coffee][https://img.shields.io/badge/support-buymeacoffee-222222.svg?style=flat-square]][https://www.buymeacoffee.com/lorenzodeluca]

> Silence.eco Scooter data for [Home Assistant][https://www.home-assistant.io]

This is a Home Assistant custom component that integrate data from you Silence Scooter to Home Assistant.
If you like this project you can support me with :coffee: or simply put a :star: to this repository :blush:

<a href="https://www.buymeacoffee.com/lorenzodeluca" target="_blank">
  <img src="https://www.buymeacoffee.com/assets/img/custom_images/yellow_img.png" alt="Buy Me A Coffee" width="150px">
</a>

# Disclaimer
This plugin was developed by analyzing traffic from official Silence Connected App, it was not sponsored or officially supported by Silence.eco
If someone from Silence would like to contribute or collaborate please contact me at [me@lorenzodeluca.dev](mailto:me@lorenzodeluca.dev?subject=[GitHub]Ha-Silence)

# Home Assistant
After installing and configuring the plugin you will be able to view on home assistant all the data of your scooter silence, 
keep statistics and use them for your automations.

![HA Entities](https://raw.githubusercontent.com/lorenzo-deluca/homeassistant-silence/master/images/ha-entities.png)
![HA Battery Soc](https://raw.githubusercontent.com/lorenzo-deluca/homeassistant-silence/master/images/ha-batterysoc.png)

## Installation
You can install this plugin like any other hacs integration on home assistant.

### HACS
- Add repository "https://github.com/lorenzo-deluca/homeassistant-silence" to custom repositories and select "Integration" category.
- Click on "Install" in the plugin card.

### Manual
Copy or link [`silence-scooter`](./custom_components/silence-scooter) subfolder to `config/custom_components`.

## Configuration
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

## License
GNU AGPLv3 © [Lorenzo De Luca][https://lorenzodeluca.dev]