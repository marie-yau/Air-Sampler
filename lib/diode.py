"""
Package for diode.
"""

import RPi.GPIO as GPIO
import settings
import validate
import time
import logging

class Diode():
    """
    Class for setting a diode.
    """
    __slots__ = ["diode_pin_number", "diode_on", "mode"]

    def __init__(self, diode_pin_number, mode, logger):
        settings.set_board_numbering_mode(mode)
        self.mode = mode
        self.set_diode_pin_number(diode_pin_number)
        self.__diode_setup()
        # TODO: verify that logger is a logging object, not sure how to do that assert(isinstance(logger, ???)
        self.logger = logger

    def set_diode_pin_number(self, diode_pin_number):
        """
        :param diode_pin_number: Integer that represent the GPIO pin number that the diode is connected to
        """
        assert(validate.is_valid_GPIO_pin_number(diode_pin_number, self.mode))
        self.diode_pin_number = diode_pin_number
        self.logger.info("diode: pump GPIO number set to {} {}".format(self.diode_pin_number, self.mode))

    def __pump_setup(self):
        """
        Sets the specified GPIO pin as an output pin.
        """
        GPIO.setup(self.diode_pin_number, GPIO.OUT)
        self.diode_on = False

    def turn_diode_on(self):
        GPIO.output(self.diode_pin_number, 1)
        self.diode_on = True
        self.logger.info("diode: diode turned on")

    def turn_diode_on_for(self, number_of_seconds):
        assert(isinstance(number_of_seconds, int))
        self.turn_diode_on()
        time.sleep(number_of_seconds)
        self.turn_diode_off()

    def turn_diode_off(self):
        GPIO.output(self.diode_pin_number, 0)
        self.diode_on = False
        self.logger.info("diode: diode turned off")

    def is_on(self):
        """
        :return: True when the diode is on, False when the diode is off
        """
        return self.diode_on


if __name__ == "__main__":
    diode_pin_number = 27
    numbering_mode = "BCM"
    diode = Diode(diode_pin_number, numbering_mode)
    diode.turn_diode_on()
    time.sleep(5)
    diode.turn_diode_off()