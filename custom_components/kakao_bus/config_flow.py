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
            bus_stop_name = user_input[CONF_BUS_STOP_NAME]
            bus_stop_id = user_input[CONF_BUS_STOP_ID]
            title = f"{bus_stop_name} ({bus_stop_id})"

            return self.async_create_entry(
                title=title,
                data={
                    CONF_BUS_STOP_ID: bus_stop_id,
                    CONF_BUS_STOP_NAME: bus_stop_name,
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