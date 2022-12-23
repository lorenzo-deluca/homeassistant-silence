"""Integration for Silence Scooters by Lorenzo De Luca (me@lorenzodeluca.dev)"""
import logging
import operator
import itertools

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_MONITORED_VARIABLES
from homeassistant.const import (CONF_NAME, STATE_UNKNOWN)
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.exceptions import PlatformNotReady
from homeassistant.helpers.entity import Entity

import homeassistant.helpers.config_validation as cv

from .const import (CONF_USERNAME, CONF_PASSWORD, CONF_API_KEY, DEFAULT_NAME, ATTR_MEASUREMENT_DATE, ATTR_UNIT_OF_MEASUREMENT, DOMAIN_DATA)
from .const import SENSOR_TYPES
from .api import SilenceApiData

_LOGGER = logging.getLogger(__package__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_USERNAME, default=CONF_USERNAME): cv.string,
    vol.Optional(CONF_PASSWORD, default=CONF_PASSWORD): cv.string,
    vol.Optional(CONF_API_KEY, default='AIzaSyAVnxe4u3oKETFWGiWcSb-43IsBunDDSVI'): cv.string,
})

def setup_platform(hass, config, add_entities, discovery_info=None):

    try:
        name = config.get(CONF_NAME)
        username = config.get(CONF_USERNAME)
        password = config.get(CONF_PASSWORD)
        apikey = config.get(CONF_API_KEY)

        silence_api = SilenceApiData(username,password,apikey)
        silence_api.update()

        if silence_api is None:
            raise PlatformNotReady("silence_api not ready!")
    except:
        raise PlatformNotReady("Error while setup platform!")

    # add sensors
    devices = []
    for sensor in SENSOR_TYPES:
        sensor_config = SENSOR_TYPES[sensor]
        devices.append(
            SilenceSensor(
                silence_api,
                sensor,
                sensor_config[0],
                sensor_config[1],
                sensor_config[2],
                sensor_config[3],
            )
        )
    add_entities(devices)

class SilenceSensor(Entity):
    def __init__(self, silence_api, name, sensor_id, unit_of_measurement, device_class, icon):
        self._json_data = silence_api
        self._name = 'silence.' + name
        self._fieldname = sensor_id
        self._measurement_date = None
        self._state = None
        self._unit_of_measurement = unit_of_measurement
        self._icon = icon
        self._device_class = device_class

    @property
    def name(self):
        return self._name

    @property
    def device_class(self):
        return self._device_class

    @property
    def icon(self):
        return self._icon

    @property
    def state(self):
        return self._state

    @property
    def measurement_date(self):
        return self._measurement_date

    @property
    def unit_of_measurement(self):
        return self._unit_of_measurement
        
    @property
    def extra_state_attributes(self):
        return{
            ATTR_MEASUREMENT_DATE: self._measurement_date,
            ATTR_UNIT_OF_MEASUREMENT: self._unit_of_measurement
        }

    @property
    def unique_id(self):
        return self._name

    @property
    def type(self):
        return 'auto'

    @property
    def id(self):
        return self._name

    def update(self):
        #if self._fieldname == 'dummy_command':
        #    _LOGGER.error(f"update - receive command {self.state}")
        #else:
            """Get the latest data from the Silence API."""
            self._json_data.update()
            data = self._json_data.result

            if data is None or self._fieldname not in data:
                self._state = STATE_UNKNOWN
            else:
                self._state = data[self._fieldname]
                self._measurement_date = data["lastReportTime"]
