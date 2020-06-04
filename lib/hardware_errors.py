"""
Custom errors and exceptions that are raised when there is a problem with hardware configuration
"""


class HardwareConfigurationFileError(Exception):
    """
    Error that is raised when there is a problem with a hardware configuration file
    """
    def __init__(self, file_path, message):
        self.file_path = file_path
        self.message = message

    def __str__(self):
        return "Invalid hardware configuration file ({}) - {}".format(self.file_path, self.message)


class HardwareConfigurationError(Exception):
    """
    Error that is raised when there is a problem with hardware configuration
    """
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "Invalid hardware configuration - {}".format(self.message)


if __name__ == "__main__":
    raise HardwareConfigurationFileError("/pi/home/config.txt", "Diode pin number is not specified.")
    raise HardwareConfigurationError("Pin number 18 is already used.")