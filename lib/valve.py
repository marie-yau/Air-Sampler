"""
Package for a valve.
"""

import RPi.GPIO as GPIO
import time
import settings
import validate

class Valve():
    """
    Class for storing information about a valve event.
    """
    __slots__ = ["valve_pin_number", "valve_open", "mode", "logger"]

    def __init__(self, valve_pin_number, mode, logger):
        # TODO: verify that logger is a logging object, not sure how to do that assert(isinstance(logger, ???)
        self.logger = logger
        # set board numbering mode
        settings.set_board_numbering_mode(mode)
        self.mode = mode
        self.set_valve_pin_number(valve_pin_number)
        self.__valve_setup()

    def set_valve_pin_number(self, valve_pin_number):
        assert(validate.is_valid_GPIO_pin_number(valve_pin_number, self.mode))
        self.valve_pin_number = valve_pin_number
        self.logger.info("valve: valve GPIO number set to {} {}".format(self.valve_pin_number, self.mode))

    def __valve_setup(self):
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