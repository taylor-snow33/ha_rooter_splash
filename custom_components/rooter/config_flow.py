"""Config flow for ROOTer."""
import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_VERIFY_SSL
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import RooterApiClient
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST, default="192.168.10.1"): str,
        vol.Optional(CONF_VERIFY_SSL, default=False): bool,
    }
)

class RooterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ROOTer."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            self._async_abort_entries_match({CONF_HOST: user_input[CONF_HOST]})

            session = async_get_clientsession(self.hass)
            client = RooterApiClient(
                session=session,
                host=user_input[CONF_HOST],
                verify_ssl=user_input[CONF_VERIFY_SSL],
            )

            try:
                await client.async_get_data()
            except Exception:
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(
                    title=f"ROOTer ({user_input[CONF_HOST]})",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )
