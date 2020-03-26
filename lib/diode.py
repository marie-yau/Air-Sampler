"""
Package for diode.
"""

import RPi.GPIO as GPIO
import time
import logging
from datetime import timedelta

import settings
import validate

class Diode():
    """
    Class for setting a diode.
    """
    __slots__ = ["diode_pin_number", "diode_on", "mode", "logger", "diode_light_duration"]

    def __init__(self, diode_pin_number, mode, logger):
        """
        :param diode_pin_number: integer representing the GPIO pin number that the diode is connected to
        :param mode: string representing the Pi's numbering mode, must be "BCM" or "BOARD"
        :param logger: `logging.Logger` object used for logging actions of the object
        """
        self.set_logger(logger)
        settings.set_board_numbering_mode(mode)
        self.mode = mode
        self.set_diode_pin_number(diode_pin_number)
        self.__diode_setup()

    def set_logger(self, logger):
        """
        :param logger: `logging.Logger` object used for logging actions of the object
        """
        assert(isinstance(logger, logging.Logger))
        self.logger = logger

    def set_diode_pin_number(self, diode_pin_number):
        """
        :param diode_pin_number: integer representing the GPIO pin number that the diode is connected to
        """
        assert(validate.is_valid_GPIO_pin_number(diode_pin_number, self.mode))
        self.diode_pin_number = diode_pin_number
        self.logger.info("diode.py: pump GPIO number set to {} {}".format(self.diode_pin_number, self.mode))

    def __diode_setup(self):
        """
        Sets the specified GPIO pin as an output pin.
        """
        GPIO.setup(self.diode_pin_number, GPIO.OUT)
        self.diode_on = False

    def set_diode_light_duration(self, duration):
        """
        :param duration: `datetime` object representing the number of seconds that diode stays turned on
        """
        assert(isinstance(duration, timedelta))
        self.diode_light_duration = duration

    def get_diode_light_duration_in_seconds(self):
        """
        :return: float representing the number of seconds that diode stays turned on
        """
        return self.diode_light_duration.total_seconds()

    def turn_diode_on(self):
        GPIO.output(self.diode_pin_number, 1)
        self.diode_on = True
        self.logger.info("diode.py: diode turned on")

    def turn_diode_on_for(self, number_of_seconds):
        """
        Turns diode on for specified number of seconds.
        :param number_of_seconds: float representing the number of seconds that diode stays turned on
        """
        assert(isinstance(number_of_seconds, float))
        self.turn_diode_on()
        time.sleep(number_of_seconds)
        self.turn_diode_off()

    def turn_diode_off(self):
        GPIO.output(self.diode_pin_number, 0)
        self.diode_on = False
        self.logger.info("diode: diode turned off")

    def diode_is_on(self):
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