"""
Store information about sampler configuration
"""

import logging

from hardware_errors import *
import validate


class HardwareConfiguration():
    """
    Class for reading hardware configuration from a text file.
    Refer to the documentation for information on the required file format.

    Sample hardware configuration file:
    ---------------------
    Identification number
    9
    Numbering mode
    BCM
    Bag numbers to valve pin numbers
    1: 19, 2: 4
    Pump pin number
    13
    Diode pin number
    17
    ---------------------
    """

    __slots__ = ["identification_number", "numbering_mode", "bag_numbers_to_valve_pin_numbers_dict",
                 "pump_pin_number", "diode_pin_number", "logger"]

    def __init__(self, file_path, logger):
        """
        :param file_path: string representing path to hardware configuration file
        :param logger: `logging.Logger` object used for logging actions of the object
        """
        self.set_logger(logger)
        self.__read_hardware_configuration_file(file_path)

    def __read_hardware_configuration_file(self, file_path):
        """
        Reads hardware configuration file and sets class attributes to specified values.
        If the file is in an incorrect format, it will raise `HardwareConfigurationFileError` or
        `HardwareConfigurationFileErrors`.
        :param file_path: string representing path to hardware configuration file
        """
        try:
            with open(file_path, "r") as config_file:
                lines = [line.strip() for line in config_file]
        except FileNotFoundError:
            raise HardwareConfigurationFileError(file_path, "Configuration file is missing.")

        error_messages = []
        # identification number section
        try:
            if lines[0] != "Identification number":
                error_messages.append("- Line 1: Invalid header."
                                      "\n + Expected `Identification number`")
            self.__set_identification_number(lines[1])
        except:
            error_messages.append("- Line 2: Invalid identification number."
                                  "\n + Expected a positive integer")
        # numbering mode section
        try:
            if lines[2] != "Numbering mode":
                error_messages.append("- Line 3: Invalid header."
                                      "\n + Expected `Numbering mode`")
            self.__set_numbering_mode(lines[3])
        except:
            error_messages.append("- Line 4: Invalid numbering mode."
                                  "\n + Expected `BCM` or `BOARD`")
        # bag numbers to valve pin numbers
        try:
            if lines[4] != "Bag numbers to valve pin numbers":
                error_messages.append("- Line 5: Invalid header."
                                      "\n + Expected `Bag numbers to valve pin numbers`")
            self.__set_bag_numbers_to_valve_pin_numbers_dict(lines[5])
        except:
            error_messages.append("- Line 6: Invalid bag numbers to valve pin numbers."
                                  "\n + Expected `<bag #1> : <pin #1>, ..., <bag #n> : <pin #n>`"
                                  "\n + Bag numbers must be positive integers"
                                  "\n + Valve pin numbers must be valid GPIO numbers in the specified numbering mode"
                                  "\n + E.g. `1: 19, 2: 4, 3: 22`")
        # pump pin number section
        try:
            if lines[6] != "Pump pin number":
                error_messages.append("- Line 7: Invalid header."
                                      "\n + Expected `Pump pin number`")
            self.__set_pump_pin_number(lines[7])
        except:
            error_messages.append("- Line 8: Invalid pump pin number."
                                  "\n + Expected a valid GPIO number in the specified numbering mode")
        # diode pin number section
        try:
            if lines[8] != "Diode pin number":
                error_messages.append("- Line 9: Invalid header."
                                      "\n + Expected `Diode pin number`")
            self.__set_diode_pin_number(lines[9])
        except:
            error_messages.append("- Line 10: Invalid diode pin number."
                                  "\n + Expected a valid GPIO number in the specified numbering mode")

        # check if hardware configuration file contains any additional lines
        if len(lines) > 10:
            for i in range(10,len(lines)):
                if lines[i].strip() != "":
                    error_messages.append("- Line {}: Extra lines are not allowed."
                                          "\n + Delete this line")
        # check if all pin numbers are unique
        try:
            pin_numbers = [self.diode_pin_number, self.pump_pin_number]
            pin_numbers.extend(list(self.bag_numbers_to_valve_pin_numbers_dict.values()))
            if HardwareConfiguration.nonunique_pin_numbers(pin_numbers):
                error_messages.append("- {} pin numbers are used multiple times."
                                      "\n + All pin number must be unique"
                                      .format(HardwareConfiguration.nonunique_pin_numbers(pin_numbers)))
        except:
            pass

        if error_messages:
            raise HardwareConfigurationFileErrors(file_path, error_messages)

    @staticmethod
    def nonunique_pin_numbers(pin_numbers):
        """
        Returns list of non-unique numbers in the list.
        :param pin_numbers: list of integers representing pin numbers
        :return list of integers that appeared more than once in `pin_numbers`
        """
        duplicates = set([x for x in pin_numbers if pin_numbers.count(x) > 1])
        return duplicates

    def set_logger(self, logger):
        """
        :param logger: `logging.Logger` object used for logging actions of `Configuration` object
        """
        assert (isinstance(logger, logging.Logger))
        self.logger = logger

    def __set_identification_number(self, id):
        """
        :param id: string representing identification number
        """
        assert (int(id) > 0)
        self.identification_number = int(id)

    def __set_numbering_mode(self, mode):
        """
        :param mode: string representing Pi's numbering mode, must be "BCM" or "BOARD"
        """
        assert (mode == "BCM" or mode == "BOARD")
        self.numbering_mode = mode
        self.logger.info("configuration.py: set numbering mode to {}".format(self.numbering_mode))

    def __set_bag_numbers_to_valve_pin_numbers_dict(self, line):
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
            assert (validate.is_valid_GPIO_pin_number(valve_number, self.numbering_mode))
            self.bag_numbers_to_valve_pin_numbers_dict[bag_number] = valve_number
        self.logger.info("configuration.py: set bag numbers to GPIO number dictionary to {}"
                         .format(self.bag_numbers_to_valve_pin_numbers_dict))

    def __set_pump_pin_number(self, pin):
        """
        :param pin: string representing the GPIO pin number that the pump is connected to
        """
        pin_number = int(pin)
        assert (validate.is_valid_GPIO_pin_number(pin_number, self.numbering_mode))
        self.pump_pin_number = pin_number
        self.logger.info("configuration.py: set pump GPIO number to {}".format(self.pump_pin_number))

    def __set_diode_pin_number(self, pin):
        """
        :param pin: string representing the GPIO pin number that the diode is connected to
        """
        pin_number = int(pin)
        assert (validate.is_valid_GPIO_pin_number(pin_number, self.numbering_mode))
        self.diode_pin_number = pin_number
        self.logger.info("configuration.py: set diode GPIO pin number to {}".format(self.diode_pin_number))

    def get_identification_number(self):
        """
        :return: integer representing identification number
        """
        return self.identification_number

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


if __name__ == "__main__":
    file_path = "../Tests/valid_hardware_configuration_file.txt"
    logger = logging.getLogger()
    hardware_config = HardwareConfiguration(file_path, logger)
    print("ID: {}\nMode: {}\nBag numbers to valve pins: {}\nPump: {}\nDiode: {}"
          .format(hardware_config.get_identification_number(),
                  hardware_config.get_numbering_mode(),
                  hardware_config.get_bag_numbers_to_valve_pin_numbers_dict(),
                  hardware_config.get_pump_pin_number(),
                  hardware_config.get_diode_pin_number()))