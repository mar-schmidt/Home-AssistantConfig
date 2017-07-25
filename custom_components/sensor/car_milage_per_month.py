# Requires jprops (pip install jprops)

"""
Configuration:

To use the car_milage_per_month component you will need to add the following to your
configuration.yaml file:

car_milage_per_month:
  odometer_sensor: sensor.ete123_odometer (the sensor that holds the total amount of km)

"""
import json
import logging
import jprops
import calendar
import os
import voluptuous as vol
import homeassistant.helpers.config_validation as cv


from datetime import datetime
from homeassistant.const import (
    CONF_NAME,
    CONF_UNIT_OF_MEASUREMENT,
    LENGTH_KILOMETERS, 
    STATE_UNKNOWN
)
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.core import HomeAssistant, CoreState

_LOGGER = logging.getLogger(__name__)
DEFAULT_NAME = 'car_milage_per_month'
DOMAIN = 'car_milage_per_month'
CONF_ODOMETER_SENSOR = 'odometer_sensor'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_ODOMETER_SENSOR): cv.entity_id,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_UNIT_OF_MEASUREMENT): cv.string
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    odometer_entity = config.get(CONF_ODOMETER_SENSOR)
    name = config.get(CONF_NAME)
    unit = config.get(CONF_UNIT_OF_MEASUREMENT)
    data = CarMilageData(hass, odometer_entity)

    add_devices([CarMilageSensor(hass, odometer_entity, name, unit, data)])


class CarMilageSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass, odometer_entity, name, unit_of_measurement, data):
        """Initialize the sensor."""
        self._hass = hass
        self._odometer_entity = odometer_entity
        self._name = name
        self._unit_of_measurement = unit_of_measurement
        self._state = STATE_UNKNOWN
        self.data = data

        self.update()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit_of_measurement

    @property
    def device_state_attributes(self):
        """Return device specific state attributes."""
        return self.data.values

    def update(self):
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        if self._hass.state not in (CoreState.starting, CoreState.not_running):
            self.data.update()
            value = self.data.values

class CarMilageData(object):
    """docstring for CarMilageData"""
    def __init__(self, hass, odometer_entity):
        self.values = {
        'last_known_value': 0,
        'current_month': 0, 
        calendar.month_name[1]: 0,
        calendar.month_name[2]: 0,
        calendar.month_name[3]: 0,
        calendar.month_name[4]: 0,
        calendar.month_name[5]: 0,
        calendar.month_name[6]: 0,
        calendar.month_name[7]: 0,
        calendar.month_name[8]: 0,
        calendar.month_name[9]: 0,
        calendar.month_name[10]: 0,
        calendar.month_name[11]: 0,
        calendar.month_name[12]: 0
        }

        self.hass = hass
        self.odometer_entity = odometer_entity

        self.milageFile = '/home/pi/.homeassistant/milage.json'
        # Create the file if not exist
        if not os.path.exists(self.milageFile):
            with open(self.milageFile, 'w') as milage:
                json.dump(self.values, milage)

    def update(self):
        odometer_value = self.getOdometerValueFromEntity(self.odometer_entity)
        self.setLastKnownValue(odometer_value)

        self.values['last_known_value'] = self.getLastKnownValue()
        self.values['current_month'] = self.getMilageCurrentMonth()
        for i in range(1, 12):
            self.values[calendar.month_name[i]] = self.getMilageForMonth(i)
            _LOGGER.info("Updating attribute %s with value %s from file", calendar.month_name[i], self.values[calendar.month_name[i]])
        
        _LOGGER.info("%s", self.values)

    def getMilageCurrentMonth(self):
        currentMonth = str(datetime.now().month).lstrip("0")
        return self.getMilageForMonth(currentMonth)
        

    def getMilageForMonth(self, month):
        monthName = calendar.month_name[int(month)]
        with open(self.milageFile) as milage:
            data = json.load(milage)
            for key, value in data.items():
                if str(key) == str(monthName):
                    return value

    def getOdometerValueFromEntity(self, entity):
        odometer_value = self.hass.states.get(entity)
        return odometer_value.state

    def getLastKnownValue(self):
        with open(self.milageFile) as milage:
            data = json.load(milage)
            return data['last_known_value']

    def setLastKnownValue(self, odometer_value):
        _LOGGER.info("Updating last_known_value to: %s", odometer_value)

        with open(self.milageFile, 'r') as milage:
            data = json.load(milage)
            data['last_known_value'] = odometer_value

        os.remove(self.milageFile)
        with open(self.milageFile, 'w') as milage:
            json.dump(data, milage)









