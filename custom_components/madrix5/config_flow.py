import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, DEFAULT_PORT, SUPPORTED_PROTOCOLS

class MadrixConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, info=None):
        if info is not None:
            return self.async_create_entry(title=f"MADRIX 5 ({info.get('host')})", data=info)

        schema = vol.Schema({
            vol.Required('host'): str,
            vol.Optional('port', default=DEFAULT_PORT): int,
            vol.Optional('protocol', default='http'): vol.In(SUPPORTED_PROTOCOLS),
            vol.Optional('api_key', default=''): str
        })

        return self.async_show_form(step_id='user', data_schema=schema)
