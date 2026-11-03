"""Raw Tuya property sensors."""
from homeassistant.components.sensor import SensorDeviceClass,SensorEntity,SensorStateClass
from homeassistant.const import PERCENTAGE,UnitOfTemperature
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN,PROPERTY_TO_DP
SENSORS={"smoke_sensor_state":("Smoke Sensor State",None,None,None),"battery_percentage":("Battery",SensorDeviceClass.BATTERY,PERCENTAGE,SensorStateClass.MEASUREMENT),"muffling":("Muffling",None,None,None),"temp_current":("Temperature",SensorDeviceClass.TEMPERATURE,UnitOfTemperature.CELSIUS,SensorStateClass.MEASUREMENT),"humidity_value":("Humidity",SensorDeviceClass.HUMIDITY,PERCENTAGE,SensorStateClass.MEASUREMENT),"temp_alarm":("Temperature Alarm Value",None,None,None),"self_test":("Self Test",None,None,None)}
async def async_setup_entry(hass,entry,async_add_entities):
    c=hass.data[DOMAIN][entry.entry_id]; async_add_entities(TuyaPropertySensor(c,entry,k) for k in SENSORS)
class TuyaPropertySensor(CoordinatorEntity,SensorEntity):
    _attr_has_entity_name=True
    def __init__(self,c,entry,key):
        super().__init__(c); self._key=key
        name,dc,unit,sc=SENSORS[key]; self._attr_name=name; self._attr_device_class=dc; self._attr_native_unit_of_measurement=unit; self._attr_state_class=sc
        did=entry.data["device_id"]; self._attr_unique_id=f"{did}_{key}"
        self._attr_device_info=DeviceInfo(identifiers={(DOMAIN,did)},name=entry.data["device_name"],manufacturer="Tuya",model="Wi-Fi smoke detector")
    @property
    def native_value(self):
        value=self.coordinator.data.get(self._key)
        return value/10 if self._key=="temp_current" and isinstance(value,(int,float)) else value
    @property
    def extra_state_attributes(self): return {"tuya_dp":PROPERTY_TO_DP[self._key],"raw_value":self.coordinator.data.get(self._key)}
