from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    add_entities([
        MadrixStatusSensor(coordinator, 'status'),
        MadrixStatusSensor(coordinator, 'current_scene'),
        MadrixStatusSensor(coordinator, 'current_cue'),
    ])

class MadrixStatusSensor(SensorEntity):
    def __init__(self, coordinator, key):
        self.coordinator = coordinator
        self._attr_name = f'MADRIX {key.replace("_"," ").title()}'
        self._key = key

    @property
    def native_value(self):
        data = self.coordinator.data or {}
        if isinstance(data, dict):
            return data.get(self._key)
        return data
