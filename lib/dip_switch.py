"""
Read dual inline package (DIP) switches.
"""

import RPi.GPIO as GPIO

class DIPSwitch():
    """
    Read dual inline package (DIP) switches.
    """

    def __init__(self, dip_switch_pin_numbers, mode):
        """
        Set board numbering mode to either "BCM" or "BOARD" and initialize maximum number of Pi's pins to default value
        40.
        :param dip_switch_pin_numbers: List of at least one integer that represent unique valid pin numbers of the Pi
                that the DIP switch is connected to. The pins in the list are ordered low-to-high.
        :param mode: string that represents the board numbering mode. Must be either "BCM" or "BOARD".
        """
        self._set_mode(mode)
        self.set_max_number_of_pins(40)
        self._set_dip_switch_pin_numbers(dip_switch_pin_numbers)

    def _set_mode(self, mode):
        assert(mode == "BCM" or mode == "BOARD")
        self.mode = mode
        GPIO.setmode(GPIO.mode)

    def _set_dip_switch_pin_numbers(self, dip_switch_pin_numbers, mode):
        """
        Check if `dip_switch_pin_numbers` is a list of valid pin numbers and set `self.dip_switch_pin_numbers`.
        `dip_switch_pin_numbers` must satisfy the following conditions:
        + contains at least one integer
        + all integers in the list are greater than 0 and at most equal to `max_number_of_pins`
        + the list doesn't contain repeated integers
        :param dip_switch_pin_numbers: List of at least one integer that represents the pin numbers of the Pi that the
                DIP switch is connected to.
        """
        # possible GPIO pin numbers in BCM mode
        pins_in_BCM_mode = [2,3,4,17,27,22,10,9,11,5,6,13,19,26,14,15,18,23,24,25,8,7,12,16,20,21]
        # check if list isn't empty
        assert(len(dip_switch_pin_numbers) > 0)
        for pin_number in dip_switch_pin_numbers:
            # check if `pin_number` is integer
            assert(isinstance(pin_number, int))
            # check if the `pin_number` is physically possible
            assert((self.mode == "BCM" and pin_number in pins_in_BCM_mode) or (self.mode == "BOARD" and pin_number > 0
                                                                               and pin_number <= self.dip_switch_pin_numbers))
        self.dip_switch_pin_numbers = dip_switch_pin_numbers

    def set_max_number_of_pins(self, max_number_of_pins):
        """
        Set maximum number of pins that Pi has. User can add more pins to Pi using port expander.
        :param max_number_of_pins: maximum number of pins that Pi has
        """
        assert(max_number_of_pins > 0)
        assert (isinstance(max_number_of_pins, int))
        self.max_number_of_pins = max_number_of_pins

    def _read_switch_positions(self):
        # set up pins as inputs
        [GPIO.setup(pin_number, GPIO.IN, pull_up_down = GPIO.PUD_UP) for pin_number in self.dip_switch_pin_numbers]
        self.switch_positions = ["1" if GPIO.input(pin) else "0" for pin in self.dip_switch_pin_numbers]

    def get_switch_position(self, index):
        self._read_switch_positions()
        return self.switch_positions[index]

    def get_switch_positions(self):
        self._read_switch_positions()
        return self.switch_positions

    @staticmethod
    def convert_switch_positions_to_decimal_number(switch_positions):
        assert(len(switch_positions) > 0)
        decimal_number = 0
        factor = 1
        for i in range(8):
            assert(switch_positions[i] == "0" or switch_positions[i] == "1")
            digit = int(switch_positions[i])
            decimal_number += digit * factor
            factor *= 2
        return decimal_number

    def __del__(self):
        """
        Set all pins in `self.dip_switch_pin_numbers` as inputs.
        """
        GPIO.cleanup(self.dip_switch_pin_numbers)

if __name__ == "__main__":
    dip_switch_pin_numbers = []
    dip_switch = DIPSwitch(dip_switch_pin_numbers, "BCM")
    dip_switch_positions = dip_switch.get_switch_positions()
    decimal_number = dip_switch.convert_switch_positions_to_decimal_number(dip_switch_positions)
    print("DIP switch positions: ", dip_switch.get_switch_positions())
    print("DIP switch positions as decimal number: ", str(decimal_number))
    print("DIP switch 4th position: ", dip_switch.get_switch_position(3))
