"""
Communicate with dual inline package (DIP) switches.
"""

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

class DIPSwitch():
    def __init__(self, dip_switch_pin_numbers):
        self.dip_switch_pin_numbers = dip_switch_pins
    
    def read_switch_positions(self):
        # set up pins as inputs
        [GPIO.setup(pin_number, GPIO.IN, pull_up_down = GPIO.PUD_UP) for pin_number in self.dip_switch_pin_numbers]
        self.switch_positions = ["1" if GPIO.input(pin) else "0" for pin in self.dip_switch_pin_numbers]
        
    def get_switch_position(self, index):
        return self.switch_positions[index]
    
    def get_switch_positions(self):
        return self.switch_positions
    
    def get_
    
    def get_ID_of_sampler_in_binary(self, DIP_switch):
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
        # TODO: Rename this function, to show its generality.
        #     It reads switch positions.
        #     The fact that the intended application is to get a sampler ID, is coincidental.

        # TODO: Understand and document whether this relates to a literal DIP switch.
        #     It seems to be reading general-purpose IO pins on the RPi.
        #     Whether those are set via a DIP switch isn't rel

        # Condition pins.
        # TODO: Test.
        #     This for-loop results from a refactoring that was done without hardware for testing.
        for pin_num in DIP_switch:

            # Set up pin.  Default is high.
            # TODO: Consider breaking this out into its own function.
            #     Presumably only need to do this once, say, at time device gets initialized.
            #     And might want to read switch positions multiple times.
            #     A clean way to do this would be to create a class that encapsulates the
            #     `DIP_switch` array.
            #     When you instantiate the class, in `__init__()`, it checks for errors,
            #     then conditions the pins.
            #     Errors would be things like no pins in array, bad (physically-impossible) pin numbers, and repeated pins.
            #     Then the class would have a method to read the pins and return a binary
            #     representation of their status.
            GPIO.setup(pin_num, GPIO.IN, pull_up_down = GPIO.PUD_UP)

        # Get inputs, as strings '1' or '0'.
        binary_digits = [
            str(int(GPIO.input(pin_num)))
                # TODO: Try `'1' if GPIO.input(pin_num) is True else '0'`
            for pin_num in DIP_switch
            ]

        # concatenate the strings representing the GPIOs' inputs
        binary = ''.join(binary_digits)

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
        # TODO: Rename this function, to show its generality.
        #     It reads switch positions, and munges the results.
        #     The fact that the intended application is to get a sampler ID, is coincidental.

        # TODO: Return a decimal number.
        #     Caller can turn that into a string as desired (will be done
        #     automatically most places you'd want to do that, anyway).

        # get binary number from DIP_switch array
        # TODO: Don't call `get_ID_of_sampler_in_binary()` here.
        #     There's no need to inter-mingle the functions this way.
        #     + Should have one function to read switches.  It can return a binary number.
        #     + Then have a function, like this one, that turns the binary number into
        #         a decimal.  And arguably that function wouldn't be in this module,
        #         since it's not specific to DIP switches.
        #     One advantage to refactoring functions that way is it would make this
        #     function easy to test, even if don't have an RPi connected.
        #     In other words, want as many functions as possible to avoid connections to hardware,
        #     since that makes them easier to test.
        binary_string = get_ID_of_sampler_in_binary(DIP_switch)

        # convert the binary number to decimal
        # TODO: If `get_ID_of_sampler_in_binary()` returned a true binary number,
        #     rather than as a string,
        #     then could do this more easily.
        decimal_number = 0
        factor = 1
        for i in range(8):
            digit = int(binary_string[i])
            decimal_number += digit * factor
            factor *= 2

        # return decimal number as a string
        return str(decimal_number)


    # TODO: Add a `__main__` here, for testing.
