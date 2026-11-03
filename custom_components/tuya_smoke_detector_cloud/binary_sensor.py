"""Boolean property entities matching Xtend Tuya's self-test sensor."""
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN, PROPERTY_TO_DP

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        TuyaBooleanProperty(coordinator, entry, "self_test", "Self test"),
    ])

class TuyaBooleanProperty(CoordinatorEntity, BinarySensorEntity):
    _attr_has_entity_name = True

    def __init__(self, coordinator, entry, key, name):
        super().__init__(coordinator)
        self._key = key
        self._attr_name = name
        device_id = entry.data["device_id"]
        self._attr_unique_id = f"{device_id}_{key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, device_id)},
            name=entry.data["device_name"],
            manufacturer="Tuya",
            model="Wi-Fi smoke detector",
        )

    @property
    def is_on(self):
        value = self.coordinator.data.get(self._key)
        return value if isinstance(value, bool) else None

    @property
    def extra_state_attributes(self):
        return {"tuya_dp": PROPERTY_TO_DP[self._key], "raw_value": self.coordinator.data.get(self._key)}
