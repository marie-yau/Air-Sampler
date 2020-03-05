from os import listdir
from os.path import isfile, join

class USB_drive():
    def __init__(self, path = "/media/pi"):
        self.path = path
        self.is_inserted = False
        self.is_inserted()

    def is_inserted(self):
        inserted_USBs = [usb for usb in listdir(self.path)]
        assert(len(inserted_USBs) == 0 or len(inserted_USBs) == 1)
        if len(inserted_USBs == 0):
            self.usb_name = None
            self.is_inserted = False
        else:
            self.usb_name = inserted_USBs[0]
            self.is_inserted = True
        return self.is_inserted

    def was_reinserted(self):
        previously_was_inserted = self.is_inserted
        now_is_inserted = self.is_inserted()
        if previously_was_inserted == False and now_is_inserted == True:
            return True
        else:
            return False

    def get_list_of_files(self):
        assert(self.is_inserted())
        return [file for file in listdir(self.path) if isfile(join(self.path, self.usb_name))]

    def get_path_for_configuration_file(self, ID):
        assert(self.is_inserted())
        configuration_file = str(ID) + "_config.txt"
        path_to_configuration_file = join(self.path, self.usb_name, configuration_file)
        assert(isfile(path_to_configuration_file))
        return path_to_configuration_file

    def get_path_for_schedule_file(self, ID):
        assert(self.is_inserted())
        schedule_file = str(ID) + "_schedule.txt"
        path_to_schedule_file = join(self.path, self.usb_name, schedule_file)
        assert(isfile(path_to_schedule_file))
        return path_to_schedule_file

if __name__ == "__main__":
    my_usb = USB_drive()
    print("USB is inserted: ", my_usb.is_inserted())
    print("List of files on USB: ", my_usb.get_list_of_files())
    print("Path to configuration file: ", my_usb.get_path_for_configuration_file())
    print("Path to schedule file: ", my_usb.get_path_for_schedule_file())
