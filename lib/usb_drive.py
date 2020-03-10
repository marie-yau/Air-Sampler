from os import listdir
from os.path import isfile, join

class USB_drive():
    def __init__(self, path = "/media/pi"):
        self.path = path
        self.inserted = False
        self.is_inserted()

    def is_inserted(self):
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
        previously_was_inserted = self.inserted
        now_is_inserted = self.is_inserted()
        if previously_was_inserted == False and now_is_inserted == True:
            return True
        else:
            return False

    def get_list_of_files(self):
        assert(self.is_inserted())
        return [file for file in listdir(join(self.path, self.usb_name)) if isfile(join(self.path, self.usb_name, file))]

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
    print("Path to configuration file: ", my_usb.get_path_for_configuration_file(90))
    print("Path to schedule file: ", my_usb.get_path_for_schedule_file(90))
    while True:
        if my_usb.was_reinserted():
            print("reinserted")
            break
