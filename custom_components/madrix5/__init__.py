from .const import DOMAIN
from .coordinator import MadrixCoordinator

async def async_setup_entry(hass, entry):
    coordinator = MadrixCoordinator(hass, entry.data)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    hass.config_entries.async_setup_platforms(entry, ["light", "sensor"])
    return True

async def async_unload_entry(hass, entry):
    unload = await hass.config_entries.async_unload_platforms(entry, ["light", "sensor"])
    if unload:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload
