# Requires jprops (pip install jprops)

"""
Configuration:

To use the car_milage_per_month component you will need to add the following to your
configuration.yaml file:

car_milage_per_month:
  odometer_sensor: sensor.ete123_odometer (the sensor that holds the total amount of km)

"""
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
    _LOGGER.info("asdasdasd %s", odometer_entity)

    add_devices([CarMilageSensor(hass, odometer_entity, name, unit, data)])

    _LOGGER.info('%s', odometer_entity)

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
        self.data.update()
        value = self.data.values

class CarMilageData(object):
    """docstring for CarMilageData"""
    def __init__(self, hass, odometer_entity):
        self.values = {
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
        _LOGGER.info("asdasdasd %s", hass)
        self.hass = hass
        _LOGGER.info("asdasdasd %s", odometer_entity)
        self.odometer_entity = odometer_entity

        self.milageFile = '/home/pi/.homeassistant/milage.properties'
        # Create the file if not exist
        if not os.path.exists(self.milageFile):
            open(self.milageFile, 'w').close()

    def update(self):
        _LOGGER.info("asdasdasd %s", self.odometer_entity)
        odometer_value = self.getOdometerValueFromEntity(self.odometer_entity)
        self.updateLastKnownValue(odometer_value)

        self.values['current_month'] = self.getMilageCurrentMonth()
        for i in range(1, 12):
            self.values[calendar.month_name[i]] = self.getMilageForMonth(i)
            _LOGGER.info("Updating month %s with value", i, self.values[calendar.month_name[i]])
        
        _LOGGER.info("%s", self.values)

    def getMilageCurrentMonth(self):
        currentMonth = str(datetime.now().month).lstrip("0")
        return self.getMilageForMonth(currentMonth)
        

    def getMilageForMonth(self, month):
        _LOGGER.debug("Getting Milage for month: %s", month)
        with open(self.milageFile) as milage:
            for key, value in jprops.iter_properties(milage):
                if int(key) == int(month):
                    _LOGGER.debug("Writing value: %s to month %s", value, month)
                    return value

    def getOdometerValueFromEntity(self, entity):
        odometer_entity = self.hass.states.get(entity)
        _LOGGER.info("%s", odometer_entity)
        return odometer_entity.state

    def updateLastKnownValue(self, odometer_value):
        with open(self.milageFile) as milage:
            _LOGGER.debug("Setting last known odometer value: %s", odometer_value)
            jprops.write_property(milage, 'last_known_value', odometer_value)