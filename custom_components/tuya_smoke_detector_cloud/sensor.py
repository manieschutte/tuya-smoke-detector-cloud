"""Tuya smoke detector property sensors."""
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity, SensorStateClass
from homeassistant.const import PERCENTAGE, UnitOfTemperature
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, PROPERTY_TO_DP

SENSORS = {
    "smoke_sensor_state": ("Smoke sensor status", None, None, None),
    "battery_percentage": ("Battery", SensorDeviceClass.BATTERY, PERCENTAGE, SensorStateClass.MEASUREMENT),
    "muffling": ("Muffling", None, None, None),
    "temp_current": ("Temperature", SensorDeviceClass.TEMPERATURE, UnitOfTemperature.CELSIUS, SensorStateClass.MEASUREMENT),
    "humidity_value": ("Humidity", SensorDeviceClass.HUMIDITY, PERCENTAGE, SensorStateClass.MEASUREMENT),
    "temp_alarm": ("Temperature alarm", None, None, None),
}

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities(TuyaPropertySensor(coordinator, entry, key) for key in SENSORS)

class TuyaPropertySensor(CoordinatorEntity, SensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, entry, key):
        super().__init__(coordinator)
        self._key = key
        name, device_class, unit, state_class = SENSORS[key]
        self._attr_name = name
        self._attr_device_class = device_class
        self._attr_native_unit_of_measurement = unit
        self._attr_state_class = state_class
        device_id = entry.data["device_id"]
        self._attr_unique_id = f"{device_id}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            name=entry.data["device_name"],
            manufacturer="Tuya",
            model="Wi-Fi smoke detector",
        )

    @property
    def native_value(self):
        value = self.coordinator.data.get(self._key)
        if self._key == "temp_current" and isinstance(value, (int, float)):
            return value / 10
        if self._key == "temp_alarm" and isinstance(value, str) and value.lower() == "cancel":
            return "None"
        return value

    @property
    def extra_state_attributes(self):
        return {"tuya_dp": PROPERTY_TO_DP[self._key], "raw_value": self.coordinator.data.get(self._key)}
