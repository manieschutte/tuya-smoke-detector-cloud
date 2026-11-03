"""Constants for Tuya Smoke Detector Cloud."""
from datetime import timedelta
DOMAIN = "tuya_smoke_detector_cloud"
DEFAULT_SCAN_INTERVAL = timedelta(seconds=60)
TUYA_API_BASE = "https://openapi.tuyaeu.com"
PROPERTY_TO_DP = {"smoke_sensor_state": 1, "battery_percentage": 15, "muffling": 16, "temp_current": 23, "humidity_value": 24, "temp_alarm": 101, "self_test": 102}
