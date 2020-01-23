"""
Read dual inline package (DIP) switches.
"""

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
    # TODO: This probably shouldn't get set here.
    #     The user should be able to decide whether to use
    #     board numbering (pin numbers on the RPi header)
    #     or BCM numbering (channel numbers on Broadcom SOC).
    #     Then user provides consistent numbers when instantiate a DIPSwitch object.
    #     The problem with setting it here is that some other bit of code
    #     may use board numbering, via `GPIO.setmode(GPIO.BOARD)`.
    #     This could create bugs that only emerge when the two modules are loaded together.

class DIPSwitch():
    """
    Read dual inline package (DIP) switches.
    """
    # TODO: Add a `__del__()` method, that performs cleanup like:
    #     GPIO.cleanup(self.dip_switch_pin_numbers)

    def __init__(self, dip_switch_pin_numbers):
        self.dip_switch_pin_numbers = dip_switch_pin_numbers
        # TODO: Document expected values for `dip_switch_pin_numbers`.
        #     E.g., it's a list (possibly an iterable) with at least one integer,
        #     integers give pin numbers for switches this instance will read,
        #     and how pin numbers are ordered (high-to-low or low-to-high bits).
        # TODO: Test `dip_switch_pin_numbers` against expectations, e.g.:
        #     assert( len(dip_switch_pin_numbers) > 0 )
        #     for pin_num in dip_switch_pin_numbers:
        #         assert( isinstance(pin_num, int) )
        #         assert( pin_num in [<list of valid pin numbers for RPi logical input>] )
        #         assert( GPIO.gpio_function(pin_num) in [GPIO.IN, GPIO.UNKNOWN] )
            # TODO: Consider copying `dip_switch_pin_numbers` in case caller mutates it for some reason.

    def read_switch_positions(self):
        # set up pins as inputs
        [GPIO.setup(pin_number, GPIO.IN, pull_up_down = GPIO.PUD_UP) for pin_number in self.dip_switch_pin_numbers]
        self.switch_positions = ["1" if GPIO.input(pin) else "0" for pin in self.dip_switch_pin_numbers]

    def get_switch_position(self, index):
        # TODO: Make this method call `read_switch_positions()`.  See more extensive comments elsewhere.
        return self.switch_positions[index]

    def get_switch_positions(self):
        # TODO: Make this method call `read_switch_positions()`.
        #     + The current design allows user to "get" positions when they haven't been "read" yet.
        #         That means currently the user must remember to call "read" before doing a "get".
        #         This places unfair burden on user.
        #     + Any time a user calls a method that returns switch positions,
        #         the switches should be read anew, in case they have changed.
        #     + Then consider renaming the read method to `_read_switch_positions()`,
        #         to show it's an internal utility method.
        return self.switch_positions

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
        # TODO: Make this method call `read_switch_positions()`.  See more extensive comments elsewhere.
        #     If do that, then `DIP_switch` is unneeded method parameter.
        #     Alternately, if want this to just be a function that takes switch values
        #     and returns binary equivalent, then make it a static method on the class
        #     (or move to a different module).

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

    def get_switch_positions_as_list(self):
        return self.switch_positions

    def get_switch_positions_as_binary_number(self):
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
        # TODO: Make this method call `read_switch_positions()`.  See more extensive comments elsewhere.
        #     If do that, then `DIP_switch` is unneeded method parameter.
        #     Alternately, if want this to just be a function that takes switch values
        #     and returns binary equivalent, then make it a static method on the class
        #     (or move to a different module).

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

    def get_switch_positions_as_decimal_number(self):
        # return decimal number
        pass

    def check_pin_numbers(self):
        # no pins in array, bad (physically-impossible) pin numbers, and repeated pins.
        pass

if __name__ == "__main__":
    pass
