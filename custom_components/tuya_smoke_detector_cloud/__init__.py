"""Integration setup."""
from __future__ import annotations
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .const import DEFAULT_SCAN_INTERVAL, DOMAIN
from .tuya_cloud import TuyaApiError, TuyaCloudClient
PLATFORMS=[Platform.SENSOR,Platform.BINARY_SENSOR]
_LOGGER=logging.getLogger(__name__)
async def async_setup_entry(hass:HomeAssistant,entry:ConfigEntry)->bool:
    client=TuyaCloudClient(async_get_clientsession(hass),entry.data["client_id"],entry.data["client_secret"])
    async def update_data():
        try: return await client.async_get_device_status(entry.data["device_id"])
        except TuyaApiError as err: raise UpdateFailed(str(err)) from err
    coordinator=DataUpdateCoordinator(hass,_LOGGER,name=entry.title,update_method=update_data,update_interval=DEFAULT_SCAN_INTERVAL)
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN,{})[entry.entry_id]=coordinator
    await hass.config_entries.async_forward_entry_setups(entry,PLATFORMS)
    return True
async def async_unload_entry(hass:HomeAssistant,entry:ConfigEntry)->bool:
    if ok:=await hass.config_entries.async_unload_platforms(entry,PLATFORMS): hass.data[DOMAIN].pop(entry.entry_id)
    return ok
