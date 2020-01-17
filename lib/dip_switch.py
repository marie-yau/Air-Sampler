"""
Communicate with dual inline package (DIP) switches.
"""


import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)


def get_ID_of_sampler_in_binary(DIP_switch):
    """
    Convert signals from DIP switch to a binary number that is used as ID of sampler.

    Parameters:

    + `DIP_switch`
        + Array of 8 integers.
        + Contains numbers of GPIO that the DIP switch is connected to (refer to Raspberry Pi layout).
        + `DIP_switch[0]` is DIP switch pin number 1, ..., `DIP_switch[7]` is DIP switch pin number 8.
        + `DIP_switch` array is read from left to right.
            E.g., array [26(off), 19(on), 13(off), 6(on), 5(on), 21(off), 20(on), 16(off)] is converted to 01011010 in binary

    Returns: binary (string)

    + String representing a binary number that was converted from DIP_switch array
    """

    # set up pins, default for the pin is high
    GPIO.setup(DIP_switch[0], GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(DIP_switch[1], GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(DIP_switch[2], GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(DIP_switch[3], GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(DIP_switch[4], GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(DIP_switch[5], GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(DIP_switch[6], GPIO.IN, pull_up_down = GPIO.PUD_UP)
    GPIO.setup(DIP_switch[7], GPIO.IN, pull_up_down = GPIO.PUD_UP)
    # get GPIOs' inputs as true and false, convert them to strings of either 1 or 0
    input_0 = str(int(GPIO.input(DIP_switch[0])))
    input_1 = str(int(GPIO.input(DIP_switch[1])))
    input_2 = str(int(GPIO.input(DIP_switch[2])))
    input_3 = str(int(GPIO.input(DIP_switch[3])))
    input_4 = str(int(GPIO.input(DIP_switch[4])))
    input_5 = str(int(GPIO.input(DIP_switch[5])))
    input_6 = str(int(GPIO.input(DIP_switch[6])))
    input_7 = str(int(GPIO.input(DIP_switch[7])))
    # concatenate the strings representing the GPIOs' inputs
    binary = input_0 + input_1 + input_2 + input_3 + input_4 + input_5 + input_6 + input_7
    # return binary number as a string
    return binary


def get_ID_of_sampler_in_decimal(DIP_switch):
    """
    Convert signals from DIP switch to a decimal number that is used as ID of sampler.

    Parameters:

    + `DIP_switch`
        + Array of 8 integers.
        + Contains numbers of GPIO that the DIP switch is connected to (refer to Raspberry Pi layout).
        + `DIP_switch[0]` is DIP switch pin number 1, ..., `DIP_switch[7]` is DIP switch pin number 8.
        + `DIP_switch` array is read from left to right.
            E.g., array [26(off), 19(on), 13(off), 6(on), 5(on), 21(off), 20(on), 16(off)] is 01011010 in binary, function converts it to 90 in decimal

    Returns: decimal_number (string)

    + String representing a decimal number that was converted from DIP_switch array
    """

    # get binary number from DIP_switch array
    binary_string = get_ID_of_sampler_in_binary(DIP_switch)
    # convert the binary number to decimal
    decimal_number = 0
    factor = 1
    for i in range(8):
        digit = int(binary_string[i])
        decimal_number += digit * factor
        factor *= 2
    # return decimal number as a string
    return str(decimal_number)    