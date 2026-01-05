"""DataUpdateCoordinator for ROOTer."""
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import RooterApiClient
from .const import DOMAIN, DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

class RooterDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching ROOTer data."""

    def __init__(self, hass: HomeAssistant, client: RooterApiClient) -> None:
        """Initialize."""
        super().__init__(
            hass=hass,
            logger=_LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.client = client

    async def _async_update_data(self) -> dict:
        """Update data via library."""
        try:
            return await self.client.async_get_data()
        except Exception as exception:
            raise UpdateFailed(exception) from exception
