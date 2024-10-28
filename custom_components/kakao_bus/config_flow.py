"""Config flow for Bus Stop integration."""
import logging
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.const import CONF_NAME

from .const import DOMAIN, CONF_BUS_STOP_ID, CONF_BUS_STOP_NAME

_LOGGER = logging.getLogger(__name__)

class BusStopConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Bus Stop."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title=user_input[CONF_BUS_STOP_NAME],
                data={
                    CONF_BUS_STOP_ID: user_input[CONF_BUS_STOP_ID],
                    CONF_BUS_STOP_NAME: user_input[CONF_BUS_STOP_NAME],
                }
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_BUS_STOP_ID): str,
                    vol.Required(CONF_BUS_STOP_NAME): str,
                }
            ),
            errors=errors,
        )