"""Platform for sensor."""
from homeassistant.helpers.entity import Entity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_BUS_STOP_ID, CONF_BUS_STOP_NAME

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up the sensor platform."""
    # Get the bus stop ID and name from the config entry data
    bus_stop_id = entry.data[CONF_BUS_STOP_ID]
    bus_stop_name = entry.data[CONF_BUS_STOP_NAME]

    # Create a sensor entity for the bus stop
    async_add_entities([BusStopSensor(hass, bus_stop_id, bus_stop_name)])

class BusStopSensor(Entity):
    """Representation of a Bus Stop sensor."""

    def __init__(self, hass, bus_stop_id, bus_stop_name):
        """Initialize the sensor."""
        self._hass = hass
        self._bus_stop_id = bus_stop_id
        self._bus_stop_name = bus_stop_name
        self._state = None
        # Add other attributes as needed

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Bus Stop {self._bus_stop_name}"

    @property
    def unique_id(self):
        """Return a unique ID for the sensor."""
        return f"{DOMAIN}_{self._bus_stop_id}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    async def async_update(self):
        """Fetch new state data for the sensor.

        This is the where you should update your sensor state based on the API data.
        """
        # Example: Fetch data from your API and update self._state
        self._state = "Some Value"