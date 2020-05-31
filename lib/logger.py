"""
Package for logging information to the log file.
"""
import usb_drive
import diode

import sys
import logging
import settings
import linecache
import time

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
    logger = logging.getLogger("main logger")
    logger.exception('Exception {} raised in file ({}, line {} "{}"): {}'.format(exception_type,
                                                                                              filename,
                                                                                              traceback.tb_lineno,
                                                                                              line.strip(),
                                                                                              exception_object))
    # set all GPIOs to output and turn them off
    settings.reset_gpio_pins()

    usb = USB_drive(logger)
    # todo - When there is an error in config file, I can’t get the diode GPIO number and numbering mode.
    #  Should I hard code it to create the diode object?
    diode = Diode(18,
                  "BCM",
                  logger)
    while True:
        # if the usb was reinserted, restart the program
        if usb.was_reinserted():
            os.execl(sys.executable, sys.executable, *sys.argv)
        # blink diode
        diode.turn_diode_on()
        time.sleep(0.5)
        diode.turn_diode_off()
        time.sleep(0.5)

if __name__ == "__main__":
    sys.excepthook = log_uncaught_exception
    result = 8 / 0
