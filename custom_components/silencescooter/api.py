import http.client
import urllib.parse
import logging
import requests
import json

from datetime import datetime, timedelta
from homeassistant.util import Throttle

MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=30)

_LOGGER: logging.Logger = logging.getLogger(__package__)

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
