import logging
from datetime import timedelta
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from .const import DOMAIN
from dataclasses import dataclass
from homeassistant.config_entries import ConfigEntry
from homeassistant.loader import Integration

from .gateways.gateway import Gateway


_LOGGER = logging.getLogger(__name__)
SCAN_INTERVAL = timedelta(minutes=10)

type ConfigEntry = ConfigEntry[Data]


class SMGwDataUpdateCoordinator(DataUpdateCoordinator):
    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        client: Gateway,
    ) -> None:
        super().__init__(
            hass=hass, logger=_LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL
        )
        self.config_entry = entry
        self.client = client

    async def _async_update_data(self):
        try:
            _LOGGER.debug("Fetching data from API")
            return await self.client.get_data()
        except Exception as e:
            _LOGGER.error(f"Error in _async_update_data: {e}")
            raise e


@dataclass
class Data:
    """Data for the Blueprint integration."""

    client: Gateway
    coordinator: SMGwDataUpdateCoordinator
    integration: Integration
