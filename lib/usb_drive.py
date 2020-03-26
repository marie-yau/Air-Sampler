"""
Package for a USB drive.
"""

from os import listdir
from os.path import isfile, join
import logging

class USB_drive():
    """
    Class for reading the configuration and schedule files.
    """

    def __init__(self, logger, path = "/media/pi"):
        """
        :param path: string representing the part to the folder where the USB drive will be mounted
        """
        self.set_logger(logger)
        self.path = path
        self.inserted = False
        self.is_inserted()

    def set_logger(self, logger):
        """
        :param logger: `logging.Logger` object used for logging actions of the object
        """
        assert (isinstance(logger, logging.Logger))
        self.logger = logger

    def is_inserted(self):
        """
        :return: True when exactly one USB drive is inserted, False when no USB drive is inserted
        """
        inserted_USBs = [usb for usb in listdir(self.path)]
        assert(len(inserted_USBs) == 0 or len(inserted_USBs) == 1)
        if len(inserted_USBs) == 0:
            self.usb_name = None
            self.inserted = False
        else:
            self.usb_name = inserted_USBs[0]
            self.inserted = True
        return self.inserted

    def was_reinserted(self):
        """
        :return: True when a USB drive previously wasn't inserted and now is inserted, False otherwise
        """
        previously_was_inserted = self.inserted
        now_is_inserted = self.is_inserted()
        if previously_was_inserted == False and now_is_inserted == True:
            self.logger.info("usb_drive.py: a new USB was inserted")
            return True
        else:
            return False

    def get_list_of_files(self):
        """
        :return: list of files on the inserted USB drive
        """
        assert(self.is_inserted())
        return [file for file in listdir(join(self.path, self.usb_name)) if isfile(join(self.path, self.usb_name, file))]

    def get_path_for_configuration_file(self, ID):
        """
        Generates path for the configuration file on the USB drive.
        :param ID: integer representing the ID number of sampler
        :return: string representing the path to the configuration file "<path_to_USB>/<ID>_config.txt>
        E.g."/media/pi/my_usb/90_config.txt"
        """
        assert(self.is_inserted())
        configuration_file = str(ID) + "_config.txt"
        path_to_configuration_file = join(self.path, self.usb_name, configuration_file)
        assert(isfile(path_to_configuration_file))
        return path_to_configuration_file

    def get_path_for_schedule_file(self, ID):
        """
        Generates path for the schedule file on the USB drive.
        :param ID: integer representing the ID number of sampler
        :return: string representing the path to the schedule file "<path_to_USB>/<ID>_schedule.txt>
        E.g."/media/pi/my_usb/90_schedule.txt"
        """
        assert(self.is_inserted())
        schedule_file = str(ID) + "_schedule.txt"
        path_to_schedule_file = join(self.path, self.usb_name, schedule_file)
        assert(isfile(path_to_schedule_file))
        return path_to_schedule_file

if __name__ == "__main__":
    my_usb = USB_drive()
    print("USB is inserted: ", my_usb.is_inserted())
    print("List of files on USB: ", my_usb.get_list_of_files())
    print("Path to configuration file: ", my_usb.get_path_for_configuration_file(90))
    print("Path to schedule file: ", my_usb.get_path_for_schedule_file(90))
    while True:
        if my_usb.was_reinserted():
            print("reinserted")
            break
