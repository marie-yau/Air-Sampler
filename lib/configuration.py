"""
Read configuration from a file.
"""

from datetime import timedelta
import logging

from invalid_file_format_errors import *

class Configuration():
    """
    Class for reading configuration from a text file.
    Refer to the documentation for information on the required file format.

    Sample configuration file:
    ----------------
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
    __slots__ = ["pump_starts_before", "pump_stops_after", "pump_time_off_tolerance", "logger", "user_logger",
                 "diode_light_duration"]

    def __init__(self, file_path, logger, user_logger):
        """
        :param file_path: string representing a path to the configuration file
        :param logger: `logging.Logger` object used for logging actions of `Configuration` object
        :param user_logger: `logging.Logger` object used for logging invalid format of configuration file
        in a user-friendly way
        """
        self.set_logger(logger)
        self.set_user_logger(user_logger)
        self.__read_configuration_file(file_path)

    def __read_configuration_file(self, file_path):
        """
        Reads configuration file line by line and sets class attributes using their setter methods.
        :param file_path: string representing a path to the configuration file
        :param user_logger: `logging.Logger` object used for logging invalid format of configuration file
        in a user-friendly way
        """
        error_messages = []

        # read lines of into a list and remove any leading and trailing white spaces
        lines = []
        try:
            with open(file_path, "r") as config_file:
                lines = [line.strip() for line in config_file]
        except:
            error_messages.append("Configuration file is missing. "
                                  "Create a valid configuration file `{}` on the USB drive. "
                                  .format(file_path.split("/")[-1]))

        # diode light duration section
        try:
            if lines[0] != "Diode light duration":
                error_messages.append("- Line 1: Header is invalid."
                                      "\n + Expected `Diode light duration`.")
            self.set_diode_light_duration(lines[1])
        except:
            error_messages.append("- Line 2: Diode light duration is invalid."
                                  "\n + Expected a positive integer.")
        # number of seconds pump starts pumping before valve opens section
        try:
            if lines[2] != "Number of seconds pump starts pumping before valve opens":
                error_messages.append("- Line 3: Header is invalid. "
                                      "\n + Expected `Number of seconds pump starts pumping before valve opens`.")
            self.set_pump_starts_before(lines[3])
        except:
            error_messages.append("- Line 4: Number of seconds that pump starts before valve opens is invalid."
                                  "\n + Expected a non-negative integer.")
        # number of seconds pump continues pumping after valve closes section
        try:
            if lines[4] != "Number of seconds pump continues pumping after valve closes":
                error_messages.append("- Line 5: Header is invalid."
                                      "\n + Expected `Number of seconds pump continues pumping after valve closes`.")
            self.set_pump_stops_after(lines[5])
        except:
            error_messages.append("- Line 6: Number of seconds pump continues pumping after valve closes is invalid."
                                  "\n + It must be a non-negative integer.")
        # pump time off tolerance in seconds
        try:
            if lines[6] != "Pump time off tolerance in seconds":
                error_messages.append("- Line 7: Header is invalid."
                                      "\n + Expected `Pump time off tolerance in seconds`.")
            self.set_pump_time_off_tolerance(lines[7])
        except:
            error_messages.append("- Line 8: Pump time off tolerance in seconds is invalid."
                                  "\n + It must be a non-negative integer.")
        # check if file contains more lines
        if len(lines) > 8:
            for i in range (8, len(lines)):
                if lines[i].strip() != "":
                    error_messages.append("- Line {}: Extra lines are not allowed."
                                          "\n + Delete this line."
                                          .format(i+1))
        # write error messages to log files
        if error_messages:
            self.logger.info("-------------")
            self.user_logger.info("CONFIGURATION FILE")
            self.logger.info("Configuration file")
            for msg in error_messages:
                self.logger.info(msg)
                self.user_logger.info(msg)
            self.logger.info("-------------")
            raise ConfigurationFileErrors(file_path, "Configuration file is missing or is in an invalid format.")

    def set_logger(self, logger):
        """
        :param logger: `logging.Logger` object used for logging actions of `Configuration` object
        """
        assert(isinstance(logger, logging.Logger))
        self.logger = logger

    def set_user_logger(self, user_logger):
        assert (isinstance(user_logger, logging.Logger))
        self.user_logger = user_logger

    def set_diode_light_duration(self, time):
        """
        :param time: string representing the number of seconds that diode stays turned on
        """
        assert(int(time) > 0)
        self.diode_light_duration = timedelta(seconds=int(time))
        self.logger.info("Configuration.py: set diode light duration to {}".format(self.diode_light_duration))

    def set_pump_starts_before(self, number_of_seconds):
        """
        :param number_of_seconds: string representing the number of seconds that the pump starts pumping before the
        valve opens
        """
        assert(int(number_of_seconds) >= 0)
        self.pump_starts_before = timedelta(seconds=int(number_of_seconds))
        self.logger.info("configuration.py: set pump starts before valve opens to {}".format(self.pump_starts_before))

    def set_pump_stops_after(self, number_of_seconds):
        """
        :param number_of_seconds: string representing the number of seconds that the pump keeps pumping after the
        valve closes
        """
        assert(int(number_of_seconds) >= 0)
        self.pump_stops_after = timedelta(seconds=int(number_of_seconds))
        self.logger.info("configuration.py: set pump stops after valve closes to {}".format(self.pump_stops_after))

    def set_pump_time_off_tolerance(self, number_of_seconds):
        """
        :param number_of_seconds: string representing the number of seconds. If pump is supposed to turn off for less
        than specified number of seconds, it will continue pumping
        """
        assert(int(number_of_seconds) >= 0)
        self.pump_time_off_tolerance = timedelta(seconds=int(number_of_seconds))
        self.logger.info("configuration.py: set pump time off tolerance to {}".format(self.pump_time_off_tolerance))

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
    file_path = "../Tests/valid_configuration.txt"
    logger = logging.getLogger("logger")
    user_logger = logging.getLogger("user logger")
    configuration = Configuration(file_path, logger, user_logger)

    print("Diode light duration:", configuration.get_diode_light_duration())
    print("Pump starts before:", configuration.get_pump_starts_before())
    print("Pump stops after:", configuration.get_pump_stops_after())
    print("Pump time off tolerance:", configuration.get_pump_time_off_tolerance())