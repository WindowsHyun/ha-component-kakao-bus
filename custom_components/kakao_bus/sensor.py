"""Platform for sensor."""
import logging
import asyncio

import aiohttp

from homeassistant.helpers.entity import Entity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from datetime import timedelta

from .const import DOMAIN, CONF_BUS_STOP_ID, CONF_BUS_STOP_NAME

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up the sensor platform."""
    bus_stop_id = entry.data[CONF_BUS_STOP_ID]
    bus_stop_name = entry.data[CONF_BUS_STOP_NAME]

    # Create a coordinator to fetch bus data
    coordinator = BusDataCoordinator(hass, bus_stop_id)

    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()

    # Create sensor entities for each bus
    sensors = []
    for bus_data in coordinator.data.get("busesList", []):
        bus_name = bus_data.get("name")
        if bus_name:
            sensors.append(BusArrivalSensor(coordinator, bus_stop_name, bus_name))
            sensors.append(BusLocationSensor(coordinator, bus_stop_name, bus_name))
    async_add_entities(sensors)

class BusDataCoordinator(DataUpdateCoordinator):
    """Data coordinator for fetching bus information."""

    def __init__(self, hass, bus_stop_id):
        """Initialize the data coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=60),  # Update interval
        )
        self.bus_stop_id = bus_stop_id

    async def _async_update_data(self):
        """Fetch bus data from your API."""
        url = f"https://m.map.kakao.com/actions/busesInBusStopJson?busStopId={self.bus_stop_id}"
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        _LOGGER.debug("Data: %s", data)
                        return data
                    else:
                        raise UpdateFailed(
                            f"Error fetching data from Kakao API: {response.status}"
                        )
        except aiohttp.ClientError as error:
            raise UpdateFailed(f"Error communicating with Kakao API: {error}") from error

class BusArrivalSensor(Entity):
    """Representation of a Bus Arrival Time sensor."""

    def __init__(self, coordinator, bus_stop_name, bus_name):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._bus_stop_name = bus_stop_name
        self._bus_name = bus_name
        self._name = f"{self._bus_stop_name} {self._bus_name} 남은시간"
        self._arrival_message = None
        self._available = False

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self):
        """Return a unique ID for the sensor."""
        return f"{DOMAIN}_{self._bus_stop_name}_{self._bus_name}_arrival"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._arrival_message

    @property
    def available(self):
        """Return True if entity is available."""
        return self._available

    @property
    def should_poll(self) -> bool:
        """Return True if entity has to be polled for state.

        False if entity pushes its state to HA.
        """
        return True # 폴링 방식으로 변경

    async def async_update(self):
        """Update the sensor state from the coordinator data."""
        await self.coordinator.async_refresh() # coordinator 업데이트
        self._available = False
        for bus_data in self.coordinator.data.get("busesList", []):
            if bus_data.get("name") == self._bus_name:
                self._arrival_message = bus_data.get("vehicleStateMessage")
                self._available = True
                break

class BusLocationSensor(Entity):
    """Representation of a Bus Current Location sensor."""

    def __init__(self, coordinator, bus_stop_name, bus_name):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._bus_stop_name = bus_stop_name
        self._bus_name = bus_name
        self._name = f"{self._bus_stop_name} {self._bus_name} 현재 정류장"
        self._current_bus_stop = None
        self._available = False

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self):
        """Return a unique ID for the sensor."""
        return f"{DOMAIN}_{self._bus_stop_name}_{self._bus_name}_location"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._current_bus_stop

    @property
    def available(self):
        """Return True if entity is available."""
        return self._available

    @property
    def should_poll(self) -> bool:
        """Return True if entity has to be polled for state.

        False if entity pushes its state to HA.
        """
        return True # 폴링 방식으로 변경

    async def async_update(self):
        """Update the sensor state from the coordinator data."""
        await self.coordinator.async_refresh() # coordinator 업데이트
        self._available = False
        for bus_data in self.coordinator.data.get("busesList", []):
            if bus_data.get("name") == self._bus_name:
                self._current_bus_stop = bus_data.get("currentBusStopName")
                self._available = True
                break