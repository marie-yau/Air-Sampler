"""
Custom errors and exceptions that are raised when there is a problem with hardware configuration
"""


class HardwareConfigurationFileError(Exception):
    """
    Error that is raised when there is a problem with a hardware configuration file
    """
    def __init__(self, file_path, message):
        """
        :param file_path: string representing a path to the hardware configuration file
        :param message: string representing an error message
        """
        self.file_path = file_path
        self.message = message

    def __str__(self):
        return "Invalid hardware configuration file ({})" \
               "\n- {}".format(self.file_path, self.message)


class HardwareConfigurationFileErrors(Exception):
    """
    Error that is raised when there are multiple problems with a hardware configuration file
    """
    def __init__(self, file_path, message_list):
        """
        :param file_path: string representing a path to the hardware configuration file
        :param message_list: list of strings representing error messages
        """
        self.file_path = file_path
        self.message_list = message_list

    def __str__(self):
        return "Invalid configuration file ({})\n{}".format(self.file_path, "\n".join(self.message_list))


class HardwareConfigurationError(Exception):
    """
    Error that is raised when there is a problem with hardware configuration
    """
    def __init__(self, message):
        """
        :param message: string representing an error message
        """
        self.message = message

    def __str__(self):
        return "Invalid hardware configuration " \
               "\n- {}".format(self.message)


if __name__ == "__main__":
    raise HardwareConfigurationFileErrors("/pi/home/config.txt", ["Invalid header", "Invalid pin number"])
    raise HardwareConfigurationFileError("/pi/home/config.txt", "Diode pin number is not specified.")
    raise HardwareConfigurationError("Pin number 18 is already used.")