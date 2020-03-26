"""
Read hardware and software configuration from a file.
"""

from datetime import timedelta
import logging

import validate

class Configuration():
    """
    Class for reading configuration from a text file. An example of the required format is below.
    The headers for the lines ("Numbering mode", "Bag numbers to valve pin numbers", etc) have to be exactly in the
    same format as listed below. No additional blank lines are allowed anywhere in the file.
    Refer to the user_manual.md for more details on file format requirements and the exact meaning of each line.
    ----------------
    Numbering mode
    BCM
    Bag numbers to valve pin numbers
    1: 19, 2: 4
    Pump pin number
    13
    Diode pin number
    17
    Diode light duration
    3
    Number of seconds pump starts pumping before valve opens
    5
    Number of seconds pump continues pumping after valve closes
    5
    Pump time off tolerance in seconds
    10
    -----------------
    """
    __slots__ = ["bag_numbers_to_valve_pin_numbers_dict", "pump_pin_number", "diode_pin_number", "numbering_mode",
                 "pump_starts_before", "pump_stops_after", "pump_time_off_tolerance", "logger",
                 "diode_light_duration"]

    def __init__(self, file_path, logger):
        """
        :param file_path: string representing a path to the configuration file
        :param logger: `logging.Logger` object used for logging actions of `Configuration` object
        """
        self.set_logger(logger)
        self._read_configuration_file(file_path)

    def _read_configuration_file(self, file_path):
        """
        Reads configuration file line by line and sets class attributes using their setter methods.
        :param file_path: string representing a path to the configuration file
        """
        # read lines of into a list and remove any leading and trailing white spaces
        with open(file_path, "r") as config_file:
            lines = [line.strip() for line in config_file]
        lines_iterator = iter(lines)
        for line in lines_iterator:
            if line == "Numbering mode":
                self.set_numbering_mode(next(lines_iterator))
            elif line == "Bag numbers to valve pin numbers":
                self.set_bag_numbers_to_valve_pin_numbers_dict(next(lines_iterator))
            elif line == "Pump pin number":
                self.set_pump_pin_number(next(lines_iterator))
            elif line == "Diode pin number":
                self.set_diode_pin_number(next(lines_iterator))
            elif line == "Diode light duration":
                self.set_diode_light_duration(next(lines_iterator))
            elif line == "Number of seconds pump starts pumping before valve opens":
                self.set_pump_starts_before(next(lines_iterator))
            elif line == "Number of seconds pump continues pumping after valve closes":
                self.set_pump_stops_after(next(lines_iterator))
            elif line == "Pump time off tolerance in seconds":
                self.set_pump_time_off_tolerance(next(lines_iterator))
            else:
                raise ValueError("invalid header line format in the configuration file")

    def set_logger(self, logger):
        """
        :param logger: `logging.Logger` object used for logging actions of `Configuration` object
        """
        assert(isinstance(logger, logging.Logger))
        self.logger = logger

    def set_numbering_mode(self, mode):
        """
        :param mode: string representing Pi's numbering mode, must be "BCM" or "BOARD"
        """
        assert(mode == "BCM" or mode == "BOARD")
        self.numbering_mode = mode
        self.logger.info("configuration.py: set numbering mode to {}".format(self.numbering_mode))

    def set_bag_numbers_to_valve_pin_numbers_dict(self, line):
        """
        The function sets a dictionary `self.bag_numbers_to_valve_pin_numbers_dict` to contain bag numbers as keys and
        their corresponding GPIO numbers as values.
        :param line: string in the format "1: 19, 2: 4". The number in front of : (e.g. 1) represents the bag number
        and the number after : (e.g. 19) represents the GPIO number that the corresponding valve is connected to. Every
        bag-GPIO pair must be separated by comma. Comma at the end of the line is not allowed.
        """
        bag_numbers_and_valve_pin_numbers = line.split(",")
        self.bag_numbers_to_valve_pin_numbers_dict = {}
        for bag_and_valve in bag_numbers_and_valve_pin_numbers:
            bag, valve = bag_and_valve.split(":")
            bag_number = int(bag.strip())
            valve_number = int(valve.strip())
            self.bag_numbers_to_valve_pin_numbers_dict[bag_number] = valve_number
        self.logger.info("configuration.py: set bag numbers to GPIO number dictionary to {}"
                         .format(self.bag_numbers_to_valve_pin_numbers_dict))

    def set_pump_pin_number(self, pin):
        """
        :param pin: string representing the GPIO pin number that the pump is connected to
        """
        pin_number = int(pin)
        assert(validate.is_valid_GPIO_pin_number(pin_number, self.numbering_mode))
        self.pump_pin_number = pin_number
        self.logger.info("configuration.py: set pump GPIO number to {}".format(self.pump_pin_number))

    def set_diode_pin_number(self, pin):
        """
        :param pin: string representing the GPIO pin number that the diode is connected to
        """
        pin_number = int(pin)
        assert(validate.is_valid_GPIO_pin_number(pin_number, self.numbering_mode))
        self.diode_pin_number = pin_number
        self.logger.info("configuration.py: set diode GPIO pin number to {}".format(self.diode_pin_number))

    def set_diode_light_duration(self, time):
        """
        :param time: string representing the number of seconds that diode stays turned on
        """
        self.diode_light_duration = timedelta(seconds=int(time))
        self.logger.info("Configuration.py: set diode light duration to {}".format(self.diode_light_duration))

    def set_pump_starts_before(self, number_of_seconds):
        """
        :param number_of_seconds: string representing the number of seconds that the pump starts pumping before the
        valve opens
        """
        self.pump_starts_before = timedelta(seconds=int(number_of_seconds))
        self.logger.info("configuration.py: set pump starts before valve opens to {}".format(self.pump_starts_before))

    def set_pump_stops_after(self, number_of_seconds):
        """
        :param number_of_seconds: string representing the number of seconds that the pump keeps pumping after the
        valve closes
        """
        self.pump_stops_after = timedelta(seconds=int(number_of_seconds))
        self.logger.info("configuration.py: set pump stops after valve closes to {}".format(self.pump_stops_after))

    def set_pump_time_off_tolerance(self, number_of_seconds):
        """
        :param number_of_seconds: string representing the number of seconds. If pump is supposed to turn off for less
        than specified number of seconds, it will continue pumping
        """
        self.pump_time_off_tolerance = timedelta(seconds=int(number_of_seconds))
        self.logger.info("configuration.py: set pump time off tolerance to {}".format(self.pump_time_off_tolerance))

    def get_numbering_mode(self):
        """
        :return: string representing Pi's numbering mode ("BCM" or "BOARD")
        """
        return self.numbering_mode

    def get_bag_numbers_to_valve_pin_numbers_dict(self):
        """
        :return: dictionary containing bag numbers (integers) as keys and corresponding GPIO numbers (integers) as values
        """
        return self.bag_numbers_to_valve_pin_numbers_dict

    def get_pump_pin_number(self):
        """
        :return: integer representing the GPIO pin number that the pump is connected to
        """
        return self.pump_pin_number

    def get_diode_pin_number(self):
        """
        :return: integer representing the GPIO pin number that the diode is connected to
        """
        return self.diode_pin_number

    def get_diode_light_duration(self):
        """
        :return: integer representing the number of seconds that diode stays turned on
        """
        return self.diode_light_duration

    def get_pump_starts_before(self):
        """
        :return: integer representing the number of seconds that the pump starts pumping before the valve opens
        """
        return self.pump_starts_before

    def get_pump_stops_after(self):
        """
        :return: integer representing the number of seconds that the pump keeps pumping after the valve closes
        """
        return self.pump_stops_after

    def get_pump_time_off_tolerance(self):
        """
        :return: integer representing the number of seconds. If pump is supposed to turn off for less than specified
        number of seconds, it will continue pumping.
        """
        return self.pump_time_off_tolerance

if __name__ == "__main__":
    file_path = "/media/pi/90AF-B6A7/90_config.txt"
    logger = logging.getLogger()
    configuration = Configuration(file_path, logger)
    
    print("Numbering mode:", configuration.get_numbering_mode())
    print("Bag numbers to valve pin numbers:", configuration.get_bag_numbers_to_valve_pin_numbers_dict())
    print("Pump pin number:", configuration.get_pump_pin_number())
    print("Diode pin number:", configuration.get_diode_pin_number())
    print("Diode light duration:", configuration.get_diode_light_duration())
    print("Pump starts before:", configuration.get_pump_starts_before())
    print("Pump stops after:", configuration.get_pump_stops_after())
    print("Pump time off tolerance:", configuration.get_pump_time_off_tolerance())