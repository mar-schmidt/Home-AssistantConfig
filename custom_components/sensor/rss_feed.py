"""
Configuration:

To use the car_milage_per_month component you will need to add the following to your
configuration.yaml file:

car_milage_per_month:
  odometer_sensor: sensor.ete123_odometer (the sensor that holds the total amount of km)

"""
import logging
import calendar
import os
import subprocess
import voluptuous as vol
import homeassistant.helpers.config_validation as cv


from datetime import datetime
from homeassistant.const import (
    CONF_NAME,
    STATE_UNKNOWN
)
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers import template
from homeassistant.exceptions import TemplateError
from homeassistant.const import (
    CONF_NAME, CONF_VALUE_TEMPLATE, CONF_UNIT_OF_MEASUREMENT, CONF_COMMAND,
    STATE_UNKNOWN)
from homeassistant.core import HomeAssistant, CoreState

_LOGGER = logging.getLogger(__name__)
DEFAULT_NAME = 'rss_feed'
DOMAIN = 'rss_feed'
CONF_COMMAND = 'command'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_COMMAND): cv.string,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_VALUE_TEMPLATE): cv.template
})

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    command = config.get(CONF_COMMAND)
    name = config.get(CONF_NAME)
    value_template = config.get(CONF_VALUE_TEMPLATE)
    if value_template is not None:
          value_template.hass = hass
    data = CommandData(hass, command)

    add_devices([CommandLineRssFeedSensor(hass, command, name, data, value_template)])


class CommandLineRssFeedSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, hass, command, name, data, value_template):
        """Initialize the sensor."""
        self._hass = hass
        self._command = command
        self._name = name
        self._state = STATE_UNKNOWN
        self.data = data
        self._value_template = value_template

        self.update()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return 0

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

class CommandData(object):
    """docstring for CommandData"""
    def __init__(self, hass, command):
        self.values = {
        'return_value': "",
        }
        self.hass = hass
        self.command = command

    def update(self):
        command_value = self.getStateValueFromEntity(self.command)
        _LOGGER.info("%s", command_value)

        self.values['return_value'] = command_value

        _LOGGER.info("%s", self.values)


    def getStateValueFromEntity(self, command):
        """
        Get the current state from the passed entity
        """
        cache = {}

        _LOGGER.info("Trying to run command: %s", command)

        if command in cache:
            prog, args, args_compiled = cache[command]
        elif ' ' not in command:
            prog = command
            args = None
            args_compiled = None
            cache[command] = (prog, args, args_compiled)
        else:
            prog, args = command.split(' ', 1)
            args_compiled = template.Template(args, self.hass)
            cache[command] = (prog, args, args_compiled)

        if args_compiled:
            try:
                args_to_render = {"arguments": args}
                rendered_args = args_compiled.render(args_to_render)
            except TemplateError as ex:
                _LOGGER.exception("Error rendering command template: %s", ex)
                return
        else:
            rendered_args = None

        if rendered_args == args:
            # No template used. default behavior
            shell = True
        else:
            # Template used. Construct the string used in the shell
            command = str(' '.join([prog] + shlex.split(rendered_args)))
            shell = True

        try:
            _LOGGER.info("Running command: %s", command)
            out = subprocess.Popen(command, shell=True)
            serviceList = out.communicate()
            return str(serviceList)
          #subprocess.check_output(command, shell=shell, timeout=15).splitlines()

        except subprocess.CalledProcessError as grepexc:
            _LOGGER.info("error code %s %s", grepexc.returncode, grepexc.output)

        except subprocess.CalledProcessError:
            _LOGGER.error("Command failed: %s", command)
        except subprocess.TimeoutExpired:
            _LOGGER.error("Timeout for command: %s", command)
