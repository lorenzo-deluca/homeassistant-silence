from datetime import datetime, timedelta
import logging
import operator
import requests
import json
import itertools
import http.client
import urllib.parse

import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (CONF_NAME, STATE_UNKNOWN)
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.exceptions import PlatformNotReady
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

import homeassistant.helpers.config_validation as cv

__version__ = '0.0.1'

_LOGGER = logging.getLogger(__name__)

CONF_USERNAME = 'username'
CONF_PASSWORD = 'password'

DEFAULT_NAME = 'Energieverbruik'
DEFAULT_DATE_FORMAT = "%y-%m-%dT%H:%M:%S"

ATTR_NAME = 'name'
ATTR_UPDATE_CYCLE = 'update_cycle'
ATTR_ICON = 'icon'
ATTR_MEASUREMENT_DATE = 'date'
ATTR_UNIT_OF_MEASUREMENT = 'unit_of_measurement'

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=3600)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_USERNAME, default=CONF_USERNAME): cv.string,
    vol.Optional(CONF_PASSWORD, default=CONF_PASSWORD): cv.string,
})


def setup_platform(hass, config, add_entities, discovery_info=None):

    name = config.get(CONF_NAME)
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)

    greenchoice_api = SilenceApiData(username,password)

    greenchoice_api.update()

    if greenchoice_api is None:
        raise PlatformNotReady

    sensors = []
    sensors.append(Silence(greenchoice_api, name, username, password, "batterySoc"))
    add_entities(sensors, True)


class Silence(Entity):
    def __init__(self, greenchoice_api, name, username, password, measurement_type):
        self._json_data = greenchoice_api
        self._name = name
        self._username = username
        self._password = password
        self._measurement_type = measurement_type
        self._measurement_date = None
        self._unit_of_measurement = None
        self._state = None
        self._icon = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def icon(self):
        return self._icon

    @property
    def state(self):
        return self._state   

    @property
    def measurement_type(self):
        return self._measurement_type

    @property
    def measurement_date(self):
        return self._measurement_date

    @property
    def unit_of_measurement(self):
        return self._unit_of_measurement
        
    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return{
            ATTR_MEASUREMENT_DATE: self._measurement_date,
            ATTR_UNIT_OF_MEASUREMENT: self._unit_of_measurement
        }

    def update(self):
        """Get the latest data from the Greenchoice API."""
        self._json_data.update()

        data = self._json_data.result

        if self._username == CONF_USERNAME or self._username is None:
            _LOGGER.error("Need a username!")
        elif self._password == CONF_PASSWORD or self._password is None:
            _LOGGER.error("Need a password!")

        if data is None or self._measurement_type not in data:
            self._state = STATE_UNKNOWN
        else:
            self._state = data[self._measurement_type]
            self._measurement_date = data["lastReportTime"]

        if self._measurement_type == "batterySoc":
            self._icon = 'mdi:fire'
            self._name = 'batterySoc'
            self._unit_of_measurement = "%"


class SilenceApiData:
    def __init__(self, username, password):
        self.result = {}
        self.token = ""
        self._tokenheaders = {
            'host': 'www.googleapis.com',
            'content-type': 'application/json',
            'accept': '*/*',
            'x-firebase-locale': 'it-IT',
            'x-ios-bundle-identifier': 'co.lateralview.Silence',
            'connection': 'keep-alive',
            'x-client-version': 'iOS/FirebaseSDK/6.4.3/FirebaseCore-iOS',
            'user-agent': 'FirebaseAuth.iOS/6.4.3 co.lateralview.Silence/1.1.008 iPhone/14.4.2 hw/iPhone9_3',
            'accept-language': 'it',
            'content-length': '82',
            'accept-encoding': 'gzip, deflate, br'
        }

        self._tokenquery = json.dumps({
                "email": username,
                "returnSecureToken": True,
                "password": password
            })

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        self.result = {}

        try:
            url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=AIzaSyCQYZCPvfl-y5QmzRrbUrCwR0RVNbyKqwI"

            headers = {
                'host': 'www.googleapis.com',
                'content-type': 'application/json',
                'accept': '*/*',
                'x-firebase-locale': 'it-IT',
                'x-ios-bundle-identifier': 'co.lateralview.Silence',
                'connection': 'keep-alive',
                'x-client-version': 'iOS/FirebaseSDK/6.4.3/FirebaseCore-iOS',
                'user-agent': 'FirebaseAuth.iOS/6.4.3 co.lateralview.Silence/1.1.008 iPhone/14.4.2 hw/iPhone9_3',
                'accept-language': 'it',
                'content-length': '82',
                'accept-encoding': 'gzip, deflate, br'
            }

            response = requests.request("POST", url, headers=headers, data=self._tokenquery)
            json_result = response.json()

            _LOGGER.debug("token json_response=%s", json_result)

            if "idToken" in json_result and "error" not in json_result:
                self.token = 'Bearer ' + format(json_result['idToken'])

                try:
                    url = "https://api.connectivity.silence.eco/api/v1/me/scooters?details=true&dynamic=true"
                    payload={}
                    headers = {
                        'host': 'api.connectivity.silence.eco:443',
                        'connection': 'keep-alive',
                        'accept': '*/*',
                        'user-agent': 'Silence/220 CFNetwork/1220.1 Darwin/20.3.0',
                        'accept-language': 'it-it',
                        'authorization': self.token,
                        'accept-encoding': 'gzip, deflate, br'
                    }

                    response = requests.request("GET", url, headers=headers)
                    json_result = response.json()

                    _LOGGER._LOGGER("getsilence json_response=%s", json_result)
                    self.result["lastReportTime"] = json_result[0]["lastReportTime"]
                    self.result["batterySoc"] = json_result[0]["batterySoc"]
                except http.client.HTTPException:
                    _LOGGER.error("Could not retrieve current numbers.")
                    self.result = "Could not retrieve current numbers."
            else:
                if "error_description" in json_result:
                    error_description = json_result["error_description"]
                else:
                    error_description = "unknown"
                self.result = f"Could not retrieve token ({error_description})."
                _LOGGER.error(self.result)

        except http.client.HTTPException:
            _LOGGER.error("Could not retrieve token.")
            self.result = "Could not retrieve token."
