"""Constants for Silence Scooter Integration."""

CONF_USERNAME = 'username'
CONF_PASSWORD = 'password'
CONF_API_KEY = 'apikey'

DEFAULT_NAME = 'silencescooter'

ATTR_MEASUREMENT_DATE = 'date'
ATTR_UNIT_OF_MEASUREMENT = 'unit_of_measurement'
DOMAIN_DATA = f"{DEFAULT_NAME}_data"

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
