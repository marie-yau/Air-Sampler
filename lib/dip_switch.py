"""
Communicate with dual inline package (DIP) switches.
"""

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

class DIPSwitch():
    def __init__(self, dip_switch_pin_numbers):
        self.dip_switch_pin_numbers = dip_switch_pin_numbers

    def read_switch_positions(self):
        # set up pins as inputs
        [GPIO.setup(pin_number, GPIO.IN, pull_up_down = GPIO.PUD_UP) for pin_number in self.dip_switch_pin_numbers]
        self.switch_positions = ["1" if GPIO.input(pin) else "0" for pin in self.dip_switch_pin_numbers]

    def get_switch_position(self, index):
        return self.switch_positions[index]

    def get_switch_positions_as_list(self):
        return self.switch_positions

    def get_switch_positions_as_binary_number(self):
        # concatenate the strings representing the GPIOs' inputs
        binary = ''.join(binary_digits)


    def get_switch_positions_as_decimal_number(self):
        # return decimal number
        pass

    def check_pin_numbers(self):
        # no pins in array, bad (physically-impossible) pin numbers, and repeated pins.
        pass

if __name__ == "__main__":
    pass