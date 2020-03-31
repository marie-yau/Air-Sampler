"""
Package containing methods for setting Pi and its GPIOs.
"""

import RPi.GPIO as GPIO
import logging
import validate

from subprocess import call

def set_board_numbering_mode(mode):
    """
    Sets board numbering mode to either "BCM" (the GPIO is identified by the number that is used by Broadcom, the
    manufacturer) or "BOARD" (the GPIO is identified by the position on the Pi).
    :param mode: string representing a board numbering mode. Must be either "BCM" or "BOARD".
    """
    assert (mode == "BCM" or mode == "BOARD")
    if mode == "BCM":
        GPIO.setmode(GPIO.BCM)
    elif mode == "BOARD":
        GPIO.setmode(GPIO.BOARD)

def disable_gpio_warnings():
    """
    Disables all GPIO warnings.
    """
    GPIO.setwarnings(False)
    logging.info("settings.py: disabled GPIO warnings")

def reset_gpio_pins():
    """
    Sets all GPIO pins as output and sets the outputs to False.
    """
    disable_gpio_warnings()
    set_board_numbering_mode("BCM")
    for pin_number in range(0, 28):
        GPIO.setup(pin_number, GPIO.OUT)
        GPIO.output(pin_number, 0)
    logging.info("settings.py: set all GPIOs as output pin and set the outputs to False")


def reset_gpio_pin(pin_number, mode):
    """
    Sets specified GPIO pin as output and sets the outputs to False.
    :param pin_number: integer representing a valid GPIO pin number
    :param mode: string representing Pi's numbering mode, must be "BCM" or "BOARD"
    """
    assert(validate.is_valid_GPIO_pin_number(pin_number, mode))
    GPIO.setup(pin_number, GPIO.OUT)
    GPIO.output(pin_number, 0)
    logging.info("settings.py: set GPIO {} as output pin and set the output to False".format(pin_number))

def turn_Pi_off():
    """
    Turns Raspberry Pi off.
    """
    logging.info("settings.py: turned off Pi")
    call("poweroff", shell=True)
    
if __name__ == "__main__":
    turn_Pi_off()