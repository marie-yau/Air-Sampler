from datetime import timedelta
import os
import validate

class Configuration():
    __slots__ = ["bag_numbers_to_valve_pin_numbers_dict", "pump_pin_number", "numbering_mode",
                 "pump_starts_before", "pump_stops_after", "pump_time_off_tolerance"]
    def __init__(self, file_path):
        self._read_configuration_file(file_path)

    def _read_configuration_file(self, file_path):
        with open(file_path, "r") as config_file:
            lines = [line.strip() for line in config_file]
        lines_iterator = iter(lines)
        for line in lines_iterator:
            if line == "Numbering mode":
                self.set_numbering_mode(next(lines_iterator))
            elif line == "Bag numbers to valve pin numbers":
                self.set_bag_numbers_to_valve_pin_numbers_dict(next(lines_iterator))
            elif line == "Pump pin number":
                self.set_pump_pin_number(next(lines_iterator))
            elif line == "Number of seconds pump starts pumping before valve opens":
                self.set_pump_starts_before(next(lines_iterator))
            elif line == "Number of seconds pump continues pumping after valve closes":
                self.set_pump_stops_after(next(lines_iterator))
            elif line == "Number of seconds. If pump is supposed to turn off for less than specified number of seconds, it will continue pumping.":
                self.set_pump_time_off_tolerance(next(lines_iterator))
            else:
                raise ValueError("invalid line format in the configuration file")

    def set_numbering_mode(self, line):
        assert(line == "BCM" or line == "BOARD")
        self.numbering_mode = line

    def set_bag_numbers_to_valve_pin_numbers_dict(self, line):
        bag_numbers_and_valve_pin_numbers = line.split(",")
        self.bag_numbers_to_valve_pin_numbers_dict = {}
        for bag_and_valve in bag_numbers_and_valve_pin_numbers:
            bag, valve = bag_and_valve.split(":")
            bag_number = int(bag.strip())
            valve_number = int(valve.strip())
            self.bag_numbers_to_valve_pin_numbers_dict[bag_number] = valve_number

    def set_pump_pin_number(self, line):
        pin_number = int(line)
        assert(validate.is_valid_GPIO_pin_number(pin_number, self.numbering_mode))
        self.pump_pin_number = pin_number

    def set_pump_starts_before(self, line):
        self.pump_starts_before = timedelta(seconds=int(line))

    def set_pump_stops_after(self, line):
        self.pump_stops_after = timedelta(seconds=int(line))

    def set_pump_time_off_tolerance(self, line):
        self.pump_time_off_tolerance = timedelta(seconds=int(line))

    def get_numbering_mode(self):
        return self.numbering_mode

    def get_bag_numbers_to_valve_pin_numbers_dict(self):
        return self.bag_numbers_to_valve_pin_numbers_dict

    def get_pump_pin_number(self):
        return self.pump_pin_number

    def get_pump_starts_before(self):
        return self.pump_starts_before

    def get_pump_stops_after(self):
        return self.pump_stops_after

    def get_pump_time_off_tolerance(self):
        return self.pump_time_off_tolerance

if __name__ == "__main__":
    path = os.getcwd()
    file_path = os.path.abspath(os.path.join(path, os.pardir, "config_files", "90.txt"))
    configuration = Configuration(file_path)
    print("Numbering mode:", configuration.get_numbering_mode())
    print("Bag numbers to valve pin numbers:", configuration.get_bag_numbers_to_valve_pin_numbers_dict())
    print("Pump pin number:", configuration.get_pump_pin_number())
    print("Pump starts before:", configuration.get_pump_starts_before())
    print("Pump stops after:", configuration.get_pump_stops_after())
    print("Pump time off tolerance:", configuration.get_pump_time_off_tolerance())