from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from .api import MadrixAPI
from .const import DEFAULT_PORT, DEFAULT_PROTOCOL
import datetime

class MadrixCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, config):
        host = config.get('host')
        port = config.get('port', DEFAULT_PORT)
        protocol = config.get('protocol', DEFAULT_PROTOCOL)
        api_key = config.get('api_key', '')
        self.api = MadrixAPI(host, port=port, protocol=protocol, api_key=api_key)
        super().__init__(
            hass,
            logger=hass.logger,
            name='MADRIX 5',
            update_interval=datetime.timedelta(seconds=5),
        )

    async def _async_update_data(self):
        try:
            status = await self.api.get_status()
            return status
        except Exception as err:
            raise UpdateFailed(err) from err
