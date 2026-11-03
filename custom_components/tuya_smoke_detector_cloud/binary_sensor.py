"""Alarm binary sensors."""
from homeassistant.components.binary_sensor import BinarySensorDeviceClass,BinarySensorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN
_ACTIVE={True,1,"1","true","on","alarm","alarm_in","smoke","high"}
def active(value): return value in _ACTIVE or (isinstance(value,str) and value.lower() in _ACTIVE)
async def async_setup_entry(hass,entry,async_add_entities):
    c=hass.data[DOMAIN][entry.entry_id]
    async_add_entities([TuyaAlarm(c,entry,"smoke_sensor_state","Smoke Alarm",BinarySensorDeviceClass.SMOKE),TuyaAlarm(c,entry,"temp_alarm","Temperature Alarm",BinarySensorDeviceClass.HEAT)])
class TuyaAlarm(CoordinatorEntity,BinarySensorEntity):
    _attr_has_entity_name=True
    def __init__(self,c,entry,key,name,device_class):
        super().__init__(c); self._key=key; self._attr_name=name; self._attr_device_class=device_class
        did=entry.data["device_id"]; self._attr_unique_id=f"{did}_{key}_alarm"
        self._attr_device_info=DeviceInfo(identifiers={(DOMAIN,did)},name=entry.data["device_name"],manufacturer="Tuya",model="Wi-Fi smoke detector")
    @property
    def is_on(self): return active(self.coordinator.data.get(self._key))
    @property
    def extra_state_attributes(self): return {"raw_value":self.coordinator.data.get(self._key)}
