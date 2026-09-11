"""Config flow for ESP32 Fan integration."""
import logging

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import selector

from .devices_api import get_all_devices
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("username"): str,
        vol.Required("password"): selector.TextSelector(
            selector.TextSelectorConfig(type=selector.TextSelectorType.PASSWORD)
        ),
    }
)


async def validate_input(hass: HomeAssistant, data: dict) -> None:
    """Try authenticating to confirm username/password actually work."""
    session = aiohttp.ClientSession()
    try:
        await get_all_devices(session)
    except aiohttp.ClientError as err:
        _LOGGER.debug("Cannot authenticate: %s", err)
        raise CannotConnect from err
    finally:
        await session.close()


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ESP32 Fan."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step — the form the user fills in."""
        errors: dict[str, str] = {}

        if user_input is not None:
            # Prevent adding the same account twice
            await self.async_set_unique_id(user_input["username"])
            self._abort_if_unique_id_configured()

            try:
                await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(
                    title=f"MY DEVICES ({user_input['username']})",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect to the device."""