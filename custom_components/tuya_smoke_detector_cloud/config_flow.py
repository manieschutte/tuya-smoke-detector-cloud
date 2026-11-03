"""Config flow for Tuya Smoke Detector Cloud."""
from __future__ import annotations
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from .const import DOMAIN
from .tuya_cloud import TuyaApiError, TuyaCloudClient

class TuyaSmokeDetectorConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Configure one smoke detector."""
    VERSION = 1
    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            device_id=user_input["device_id"].strip()
            await self.async_set_unique_id(device_id); self._abort_if_unique_id_configured()
            client=TuyaCloudClient(async_get_clientsession(self.hass),user_input["client_id"].strip(),user_input["client_secret"].strip())
            try: await client.async_get_device_status(device_id)
            except TuyaApiError: errors["base"]="cannot_connect"
            else:
                name=user_input.get("device_name","").strip() or device_id
                return self.async_create_entry(title=name,data={"client_id":user_input["client_id"].strip(),"client_secret":user_input["client_secret"].strip(),"device_id":device_id,"device_name":name})
        return self.async_show_form(step_id="user",data_schema=vol.Schema({vol.Required("client_id"):str,vol.Required("client_secret"):str,vol.Required("device_id"):str,vol.Optional("device_name",default=""):str}),errors=errors)
