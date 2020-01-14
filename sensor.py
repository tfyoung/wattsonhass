"""Platform for sensor integration."""

import logging

import serial
from serial.tools.list_ports import comports
import re

from homeassistant.const import POWER_WATT, DEVICE_CLASS_POWER
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    add_entities([ExampleSensor()])

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""

    devices = []
    for port in comports():
        _LOGGER.info("Checking serial port %s", port.device)
        if port.vid != 1027 and port.pid != 24577:
            continue
        serialdev = serial.Serial(port=port.device, baudrate=19200, timeout=1)

        devices.append(UsedPower(serialdev))
        devices.append(GeneratedPower(serialdev))
        _LOGGER.info("Found Wattson on %s", port.device)
    if not devices:
        _LOGGER.info("No Wattson devices found")

    add_entities(devices)


class BaseSensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, serialdevice):
        """Initialize the sensor."""
        self._state = None
        self.serialport = serialdevice

    def runCommand(self, command):
        val = None
        retries = 0
        while val is None and retries < 3:
            self.serialport.write(command)
            val = self.serialport.readline().decode("ascii").strip()
            retries += 1
        return re.sub(r'[^\x20-\x7E]', r'', val)

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return POWER_WATT

    @property
    def device_class(self):
        return DEVICE_CLASS_POWER

class UsedPower(BaseSensor):
    def __init__(self, serialport):
        super().__init__(serialport)

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Power consumed'

    def powerUsed(self):
        p = self.runCommand(b"nowp\r")
        if p[0] != 'p':
            raise Exception("Invalid return" + p)
        return int(p[1:], 16) * 4

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self.powerUsed()

class GeneratedPower(BaseSensor):

    def __init__(self, serialport):
        super().__init__(serialport)

    @property
    def name(self):
        """Return the name of the sensor."""
        return 'Power Generated'

    def powerGenerated(self):
        p = self.runCommand(b"noww\r")
        if p[0] != 'w':
            raise Exception("Invalid return, expecting w:" + ",".join("{:02x}".format(ord(c)) for c in p))
        return int(p[1:], 16)

    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        self._state = self.powerGenerated()
