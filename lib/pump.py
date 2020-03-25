"""
Package for pump.
"""

import RPi.GPIO as GPIO
import settings
import validate
import time
import logging

class Pump():
    """
    Class for setting a pump.
    """
    __slots__ = ["pump_pin_number", "pump_on", "mode", "logger"]

    def __init__(self, pump_pin_number, mode, logger):
        # TODO: verify that logger is a logging object, not sure how to do that assert(isinstance(logger, ???)
        self.logger = logger
        # set board numbering mode for the Pi (either "BCM" or "BOARD")
        settings.set_board_numbering_mode(mode)
        self.mode = mode
        self.set_pump_pin_number(pump_pin_number)
        self.__pump_setup()

    def set_pump_pin_number(self, pump_pin_number):
        """
        :param pump_pin_number: Integer representing the GPIO pin number that the pump is connected to.
        """
        assert(validate.is_valid_GPIO_pin_number(pump_pin_number, self.mode))
        self.pump_pin_number = pump_pin_number
        self.logger.info("pump: pump GPIO number set to {} {}".format(self.pump_pin_number, self.mode))

    def __pump_setup(self):
        """
        Sets the specified GPIO pin as an output pin.
        """
        GPIO.setup(self.pump_pin_number, GPIO.OUT)
        self.pump_on = False

    def start_pumping(self):
        GPIO.output(self.pump_pin_number, 1)
        self.pump_on = True
        self.logger.info("pump: pump started pumping")

    def stop_pumping(self):
        GPIO.output(self.pump_pin_number, 0)
        self.pump_on = False
        self.logger.info("pump: pump stopped pumping")

    def is_pumping(self):
        """
        :return: True when the pump is pumping, False when pump is not pumping
        """
        return self.pump_on

if __name__ == "__main__":
    pump_pin_number = 27
    numbering_mode = "BCM"
    pump = Pump(pump_pin_number, numbering_mode)
    pump.start_pumping()
    time.sleep(10)
    pump.stop_pumping()