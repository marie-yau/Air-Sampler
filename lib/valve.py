"""
Package for a valve.
"""

import RPi.GPIO as GPIO
import time
import logging

import settings
import validate

class Valve():
    """
    Class for storing information about a valve event.
    """
    __slots__ = ["valve_pin_number", "valve_open", "mode", "logger"]

    def __init__(self, valve_pin_number, mode, logger):
        """
        :param valve_pin_number: integer representing the GPIO pin number that the valve is connected to
        :param mode: string representing the Pi's numbering mode, must be "BCM" or "BOARD"
        :param logger: `logging.Logger` object used for logging actions of the object
        """
        self.set_logger(logger)
        # set board numbering mode
        settings.set_board_numbering_mode(mode)
        self.mode = mode
        self.set_valve_pin_number(valve_pin_number)
        self.__valve_setup()

    def set_logger(self, logger):
        """
        :param logger: `logging.Logger` object used for logging actions of the object
        """
        assert(isinstance(logger, logging.Logger))
        self.logger = logger

    def set_valve_pin_number(self, valve_pin_number):
        """
        :param valve_pin_number: integer representing the GPIO pin number that the valve is connected to
        """
        assert(validate.is_valid_GPIO_pin_number(valve_pin_number, self.mode))
        self.valve_pin_number = valve_pin_number
        self.logger.info("valve: valve GPIO number set to {} {}".format(self.valve_pin_number, self.mode))

    def __valve_setup(self):
        """
        Sets the specified GPIO pin as an output pin.
        """
        GPIO.setup(self.valve_pin_number, GPIO.OUT)
        self.valve_open = False

    def open_valve(self):
        GPIO.output(self.valve_pin_number, 1)
        self.valve_open = True
        self.logger.info("valve: valve opened (GPIO number {} {})".format(self.valve_pin_number, self.mode))

    def close_valve(self):
        GPIO.output(self.valve_pin_number, 0)
        self.valve_open = False
        self.logger.info("valve: valve closed (GPIO number {} {})".format(self.valve_pin_number, self.mode))

    def valve_is_open(self):
        return self.valve_open

if __name__ == "__main__":
    valve_pin_number = 17
    numbering_mode = "BCM"
    valve = Valve(valve_pin_number, numbering_mode)
    valve.open_valve()
    time.sleep(10)
    valve.close_valve()