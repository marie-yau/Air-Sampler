"""
Package for logging information to the log file.
"""

import sys
import logging
import settings
import linecache

def log_uncaught_exception(exception_type, exception_object, traceback):
    """
    Safely exits the program by logging the exception information to the log file and resetting all GPIOs.
    :param exception_type: exception object
    :param exception_object: string representing the value of the exception
    :param traceback: traceback object
    """

    filename = traceback.tb_frame.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, traceback.tb_lineno, traceback.tb_frame.f_globals)
    logging.getLogger().exception('Exception raised in file ({}, line {} "{}"): {}'.format(filename,
                                                                                           traceback.tb_lineno,
                                                                                           line.strip(),
                                                                                           exception_object))
    # set all GPIOs to output and turn them off
    settings.reset_gpio_pins()


if __name__ == "__main__":
    sys.excepthook = log_uncaught_exception
    result = 8 / 0
