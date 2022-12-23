"""Integration for Silence Scooters by Lorenzo De Luca (me@lorenzodeluca.dev)"""
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
from homeassistant.const import CONF_MONITORED_VARIABLES
from homeassistant.const import (CONF_NAME, STATE_UNKNOWN)
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.exceptions import PlatformNotReady
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle

import homeassistant.helpers.config_validation as cv

__version__ = '0.9.3'

_LOGGER = logging.getLogger(__name__)

CONF_USERNAME = 'username'
CONF_PASSWORD = 'password'
CONF_API_KEY = 'apikey' 

DEFAULT_NAME = 'silencescooter'
DEFAULT_DATE_FORMAT = "%y-%m-%dT%H:%M:%S"

ATTR_NAME = 'name'
ATTR_UPDATE_CYCLE = 'update_cycle'
ATTR_ICON = 'icon'
ATTR_MEASUREMENT_DATE = 'date'
ATTR_UNIT_OF_MEASUREMENT = 'unit_of_measurement'
DOMAIN_DATA = f"{DEFAULT_NAME}_data"

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=30)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_USERNAME, default=CONF_USERNAME): cv.string,
    vol.Optional(CONF_PASSWORD, default=CONF_PASSWORD): cv.string,
    vol.Optional(CONF_API_KEY, default='AIzaSyAVnxe4u3oKETFWGiWcSb-43IsBunDDSVI'): cv.string,
})

SENSOR_TYPES = {
     "model": [
        "model",
        "",
        "",
        "",
    ],
     "revision": [
        "revision",
        "",
        "",
        "",
    ],
    "manufactureDate": [
        "manufactureDate",
        "",
        "date",
        "mdi:calendar",
    ],
    "imei": [
        "imei",
        "",
        "",
        "",
    ],
    "frameNo": [
        "frameNo",
        "",
        "",
        "",
    ],
    "color": [
        "color",
        "",
        "",
        "",
    ],
    "name": [
        "name",
        "",
        "",
        "",
    ],
    "batteryOut": [
        "batteryOut",
        "",
        "",
        "",
    ],
    "alarmActivated": [
        "alarmActivated",
        "",
        "",
        "",
    ],
    "charging": [
        "charging",
        "",
        "",
        "",
    ],
    "batterySoc": [
        "batterySoc",
        "%",
        "battery",
        "mdi:car-battery",
    ],
    "batteryTemperature": [
        "batteryTemperature",
        "°C",
        "temperature",
        "mdi:thermometer",
    ],
    "motorTemperature": [
        "motorTemperature",
        "°C",
        "temperature",
        "mdi:thermometer",
    ],
    "inverterTemperature": [
        "inverterTemperature",
        "°C",
        "temperature",
        "mdi:thermometer",
    ],
    "location_longitude": ["location_longitude", "lng", "none", "mdi:map-marker"],
    "location_latitude": ["location_latitude", "lat", "none", "mdi:map-marker"],
    "location_altitude": ["location_altitude", "alt", "none", "mdi:map-marker"],
    "location_currentSpeed": [
        "location_currentSpeed",
        "km/h",
        "none",
        "mdi:speedometer",
    ],
    "location_time": ["location_time", "time", "date_time_utc", "mdi:calendar"],
    "odometer": [
        "odometer",
        "km",
        "distance",
        "mdi:map-marker-distance",
    ],
    "range": [
        "range",
        "km",
        "distance",
        "mdi:map-marker-distance",
    ],
    "velocity": [
        "velocity",
        "km/h",
        "none",
        "mdi:speedometer",
    ],
    "status": [
        "status",
        "",
        "none",
        "mdi:history",
    ],
    "lastReportTime": [
        "lastReportTime",
        "",
        "date_time_utc",
        "mdi:calendar",
    ]#,
    #"dummy_command": [
    #    "dummy_command",
    #    "",
    #    "none",
    #    "",
    #]
}

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


class SilenceApiData:
    def __init__(self, username, password, apikey):
        self.result = {}
        self.token = ""
        self._apikey = apikey
        self._tokenquery = json.dumps({
                "email": username,
                "returnSecureToken": True,
                "password": password
            })
    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):

        def decode_status(status):
            if status == 0:
                return 'IDLE'
            elif status == 1:
                return 'MovingNoKey!'
            elif status == 2:
                return 'City'
            elif status == 3:
                return 'Eco'
            elif status == 4:
                return 'Sport'
            elif status == 5:
                return 'BatteryOut!'
            elif status == 6:
                return 'Charge'
            return status

        def decode_boolean(value):
            if value == 'True' or value == 'true':
                return 1
            return 0
        
        def is_running(status):
            return (status == 2 or status == 3 or status == 4 or status == 5)

        if (len(self.token) == 0):
            
            try:
                self.result = {}

                url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key="+self._apikey
                headers = {
                    'host': 'www.googleapis.com',
                    'content-type': 'application/json',
                    'accept': '*/*',
                    'x-ios-bundle-identifier': 'eco.silence.my',
                    'connection': 'keep-alive',
                    'x-client-version': 'iOS/FirebaseSDK/8.8.0/FirebaseCore-iOS',
                    'user-agent': 'FirebaseAuth.iOS/8.8.0 eco.silence.my/1.2.1 iPhone/15.6.1 hw/iPhone9_3',
                    'accept-encoding': 'gzip, deflate, br'
                }

                response = requests.request("POST", url, headers=headers, data=self._tokenquery)
                json_result = response.json()

                _LOGGER.debug("get_token json_response=%s", json_result)

                if "idToken" in json_result and "error" not in json_result:
                    self.token = 'Bearer ' + format(json_result['idToken'])
                else:
                    if "error_description" in json_result:
                        error_description = json_result["error_description"]
                    else:
                        error_description = "unknown"

                    _LOGGER.error(f"get_token - Could not find token <{self.result}>")
                    self.result = f"Error on token request ({error_description})."
                    self.token = ""
            except:
                _LOGGER.error("get_token - Could not retrieve token.")
                self.token = ""

        self.result = {}

        try:
            url = "https://api.connectivity.silence.eco/api/v1/me/scooters?details=true&dynamic=true&pollIfNecessary=true"
            payload={}
            headers = {
                'host': 'api.connectivity.silence.eco:443',
                'connection': 'keep-alive',
                'accept': '*/*',
                'user-agent': 'Silence/220 CFNetwork/1220.1 Darwin/20.3.0',
                'authorization': self.token,
                'accept-encoding': 'gzip, deflate, br'
            }

            response = requests.request("GET", url, headers=headers)
            json_result = response.json()

            _LOGGER.debug("getsilence json_response=%s", json_result)

            self.result["frameNo"] = json_result[0]["frameNo"]
            self.result["color"] = json_result[0]["color"]
            self.result["name"] = json_result[0]["name"]
            self.result["model"] = json_result[0]["model"]
            self.result["revision"] = json_result[0]["revision"]
            self.result["manufactureDate"] = json_result[0]["manufactureDate"]
            self.result["imei"] = json_result[0]["imei"]

            self.result["status"] = decode_status(json_result[0]["status"])
            self.result["alarmActivated"] = decode_boolean(json_result[0]["alarmActivated"])
            self.result["batteryOut"] = decode_boolean(json_result[0]["batteryOut"])
            self.result["charging"] = decode_boolean(json_result[0]["charging"])

            self.result["batterySoc"] = json_result[0]["batterySoc"]
            self.result["odometer"] = json_result[0]["odometer"]
            self.result["range"] = json_result[0]["range"]
            self.result["velocity"] = json_result[0]["velocity"]
            
            if is_running(json_result[0]["status"]):
                self.result["batteryTemperature"] = json_result[0]["batteryTemperature"]
                self.result["motorTemperature"] = json_result[0]["motorTemperature"]
                self.result["inverterTemperature"] = json_result[0]["inverterTemperature"]
            else:
                self.result["batteryTemperature"] = 0
                self.result["motorTemperature"] = 0
                self.result["inverterTemperature"] = 0

            self.result["location_latitude"] = json_result[0]["lastLocation"]["latitude"]
            self.result["location_longitude"] = json_result[0]["lastLocation"]["longitude"]
            self.result["location_altitude"] = json_result[0]["lastLocation"]["altitude"]
            self.result["location_currentSpeed"] = json_result[0]["lastLocation"]["currentSpeed"]
            self.result["location_time"] = json_result[0]["lastLocation"]["time"]

            self.result["lastReportTime"] = json_result[0]["lastReportTime"]

        except Exception as e:
            _LOGGER.error(f"error on update api {str(e)}")
            self.token = ""

