"""
Package for logging information to the log file.
"""

import sys
import logging
import RPi.GPIO as GPIO

import settings

def handle_uncaught_exception(exception_type, exception_value, traceback):
    """
    Handles uncaught exception and safely exits the program by logging the exception information to the log file and
    resetting all GPIOs.
    :param exception_type: Type of the exception
    :param exception_value: The value of the exception
    :param traceback: The place where the exception was raised
    """
    # write details about exception to log file
    message = "program unexpectedly terminated: " + str(exception_type) + ", " + str(exception_value) + ", " + str(traceback)
    logging.getLogger().exception(message)
    # set all GPIOs to output and turn the off
    settings.reset_gpio_pins()

if __name__ == "__main__":
    sys.excepthook = handle_uncaught_exception
    result = 8 / 0
    print(result)
