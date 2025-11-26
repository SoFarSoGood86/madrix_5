from homeassistant.components.light import LightEntity, SUPPORT_BRIGHTNESS
from .const import DOMAIN

async def async_setup_entry(hass, entry, add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    add_entities([MadrixLight(coordinator)])

class MadrixLight(LightEntity):
    def __init__(self, coordinator):
        self.coordinator = coordinator
        self._attr_name = 'MADRIX Output'
        self._is_on = False
        self._brightness = 255
        self._scene = None

    async def async_turn_on(self, **kwargs):
        # kwargs can include brightness (0-255), scene (str), cue (int)
        if 'brightness' in kwargs:
            self._brightness = kwargs['brightness']
            await self.coordinator.api.send_command('set_brightness', {'value': int(self._brightness)})
        if 'scene' in kwargs:
            self._scene = kwargs['scene']
            await self.coordinator.api.send_command('load_scene', {'name': self._scene})
        if 'cue' in kwargs:
            await self.coordinator.api.send_command('goto_cue', {'cue': int(kwargs['cue'])})
        # ensure ON command
        await self.coordinator.api.send_command('on', None)
        self._is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self):
        await self.coordinator.api.send_command('off', None)
        self._is_on = False
        self.async_write_ha_state()

    @property
    def is_on(self):
        return self._is_on

    @property
    def supported_features(self):
        return SUPPORT_BRIGHTNESS
