"""
Read dual inline package (DIP) switches.
"""

import RPi.GPIO as GPIO
import settings

class DIPSwitch():
    """
    Read dual inline package (DIP) switches.
    """

    def __init__(self, dip_switch_pin_numbers, mode):
        """
        :param dip_switch_pin_numbers: List of at least one integer that represent unique valid pin numbers of the Pi
                that the DIP switch is connected to. The pins in the list are ordered low-to-high.
                E.g. DIP switch has two switches. Switch with physical number 1 is connected to GPIO 26 and switch with
                number 2 to GPIO 19, so the `dip_switch_pin_numbers` is equal to [26,19].
        :param mode: string that represents a board numbering mode. Must be either "BCM" or "BOARD".
        """
        # set board numbering mode
        settings.set_board_numbering_mode(mode)
        self._mode = mode
        # check if `dip_switch_pin_numbers` is list of valid pin numbers
        self._set_dip_switch_pin_numbers(dip_switch_pin_numbers)

    def _set_dip_switch_pin_numbers(self, dip_switch_pin_numbers):
        """
        Check if `dip_switch_pin_numbers` is a list of valid pin numbers and set `self.dip_switch_pin_numbers`.
        :param dip_switch_pin_numbers: List of at least one integer that represents the pin numbers of the Pi that the
                DIP switch is connected to.
                `dip_switch_pin_numbers` must satisfy the following conditions:
                + contains at least one integer
                + must be a list of integers
                + pin numbers must be physically possible
                + the list doesn't contain any duplicates
        """
        # check if list contains at least one item
        assert(len(dip_switch_pin_numbers) > 0)
        # check if all items in the list are unique
        assert(len(dip_switch_pin_numbers) == len(set(dip_switch_pin_numbers)))
        for pin_number in dip_switch_pin_numbers:
            # check if `pin_number` is integer
            assert(isinstance(pin_number, int))
            # TODO: Check if the `pin_number` is physically possible.
            # The BCM pin numbers changed between different versions of Pi (revision 1 and revision 2 of Pi).
            # Should we ask user for revision number or make check more general so both rev1 and rev2 numberings can pass
            # at the same time?
            # assert((self._mode == "BCM" and pin_number >= 0 and pin_number <= 27) or (self._mode == "BOARD" and pin_number >= 1 and pin_number <= 40))
        self.dip_switch_pin_numbers = dip_switch_pin_numbers

    def _read_switch_positions(self):
        """
        Read the pin numbers of the Pi that the DIP switch is connected to and set items in the `self.switch_positions`
        list to "1" if the switch is in on position and to "0" if the switch is in off position. The switch positions
        in the `self.switch_positions` list correspond to the pin numbers in the `self.dip_switch_pin_numbers` list.
        E.g. When `self.dip_switch_pin_numbers` is equal to [26,19] and GPIO 26 is off and GPIO 19 is on, the
        `self.switch_positions` is equal to ["0","1"]
        """
        # set up pins as inputs
        [GPIO.setup(pin_number, GPIO.IN, pull_up_down = GPIO.PUD_UP) for pin_number in self.dip_switch_pin_numbers]
        self.switch_positions = ["1" if GPIO.input(pin) else "0" for pin in self.dip_switch_pin_numbers]

    def get_switch_position(self, switch_number):
        """
        Get position of specified switch in DIP switch.
        :param switch_number: Integer that represents the physical number of switch in DIP switch. The numbers of switches
                are written on the DIP switch.
        :return: "0" if switch with `switch number` is in off position or "1" if switch is in on position.
        """
        self._read_switch_positions()
        # we have to subtract 1 from `switch_number` because `self.switch_positions` is a list that starts with index 0
        # while switch numbers on DIP switch start with index 1
        return self.switch_positions[switch_number - 1]

    def get_switch_positions(self):
        """
        Get positions of all switches in DIP switch.
        :return: List of "1"s and "0"s that represent on and off positions of all switches in DIP switch. The switch
                positions in the `self.switch_positions` list correspond to the pin numbers in the
                `self.dip_switch_pin_numbers` list.
        """
        self._read_switch_positions()
        return self.switch_positions

    @staticmethod
    def convert_switch_positions_to_decimal_number(switch_positions):
        """
        Convert "1" and "0" switch positions in `switch_positions` list to a decimal number.
        E.g. list ["0","1","1"] is converted to decimal number 6.
        :param switch_positions: List of "1"s and "0"s that represent switch positions in the DIP switch. The list
                should be ordered low-to-high (position of switch with the lowest physical number should be in position
                0 in the `switch_positions` list).
        :return: Integer that represents a decimal number converted from binary number in form of list of "1" and "0".
        """
        assert(len(switch_positions) > 0)
        decimal_number = 0
        factor = 1
        for i in range(len(switch_positions)):
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
    # list GPIOs numbers in BCM mode that the DIP switch is connected to in low-to-high order
    dip_switch_pin_numbers = [26, 19, 13, 6, 5, 21, 20, 16]
    dip_switch = DIPSwitch(dip_switch_pin_numbers, "BCM")
    # get list of switch positions in the DIP switch
    dip_switch_positions = dip_switch.get_switch_positions()
    decimal_number = dip_switch.convert_switch_positions_to_decimal_number(dip_switch_positions)
    print("DIP switch positions: ", dip_switch.get_switch_positions())
    print("DIP switch positions as decimal number: ", str(decimal_number))
    print("DIP switch 4th position: ", dip_switch.get_switch_position(4))
