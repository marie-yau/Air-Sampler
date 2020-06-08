"""
Custom errors and exceptions that are raised when there is a problem with configuration file and schedule file.
"""


class ConfigurationFileError(Exception):
    """
    Error that is raised when there is a problem with a configuration file
    """
    def __init__(self, file_path, message):
        """
        :param file_path: string representing a path to a configuration file
        :param message: string representing an error message
        """
        self.file_path = file_path
        self.message = message

    def __str__(self):
        return "Invalid configuration file ({})" \
               "\n- {}".format(self.file_path, self.message)


class ConfigurationFileErrors(Exception):
    """
    Error that is raised when there are multiple problems with a configuration file
    """
    def __init__(self, file_path, message_list):
        """
        :param file_path: string representing a path to a configuration file
        :param message_list: string representing an error message
        """
        self.file_path = file_path
        self.message_list = message_list

    def __str__(self):
        return "Invalid configuration file ({})\n{}".format(self.file_path, "\n".join(self.message_list))


class ScheduleFileError(Exception):
    """
    Error that is raised when there is a problem with a schedule file
    """
    def __init__(self, file_path, message):
        """
        :param file_path: string representing a path to a schedule file
        :param message: string representing an error message
        """
        self.file_path = file_path
        self.message = message

    def __str__(self):
        return "Invalid schedule file ({})" \
               "\n- {}".format(self.file_path, self.message)


class ScheduleFileErrors(Exception):
    """
    Error that is raised when there are multiple problems with a schedule file
    """

    def __init__(self, file_path, message_list):
        """
        :param file_path: string representing a path to a schedule file
        :param message_list: string representing an error message
        """
        self.file_path = file_path
        self.message_list = message_list

    def __str__(self):
        return "Invalid schedule file ({})\n{}".format(self.file_path, "\n".join(self.message_list))


if __name__ == "__main__":
    # raise ConfigurationFileError("pi/config.txt", "File not found.")
    # raise ConfigurationFileErrors("pi/config.txt", ["Line 1: Invalid header.", "Line 2: Invalid light duration."])
    # raise ScheduleFileError("pi/schedule.txt", "File not found")
    raise ScheduleFileErrors("pi/schedule.txt", ["Line 1: Invalid start time.", "Line 2: Invalid bag number."])