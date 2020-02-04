from datetime import datetime, timedelta
import re

# TODO: Check file input.

class SamplerSchedule():
    def __init__(self, file_path, pump_delta):
        self.set_pump_delay(pump_delta)
        self.lines_in_file = self.read_lines_in_file(file_path)
        self.__convert_lines_to_valve_schedule()
        self.__convert_valve_schedule_to_pump_schedule()

    def set_pump_delay(self, pump_delta):
        assert(isinstance(pump_delta, int))
        delta = timedelta(seconds=pump_delta)
        self.pump_delta = delta

    def __convert_lines_to_valve_schedule(self):
        self.valve_schedule = []
        # e.g. 1,3; 2020-2-4, 11:30:00; 2020-2-4, 11:33:00
        for line in self.lines_in_file:
            line_without_spaces = re.sub(r"\s+", "", line, flags=re.UNICODE)
            bags, start, end = line_without_spaces.split(";")
            bag_numbers = [int(bag_number) for bag_number in bags.split(",")]
            time_on = datetime.strptime(start, "%Y-%m-%d,%H:%M:%S")
            time_off = datetime.strptime(end, "%Y-%m-%d,%H:%M:%S")
            self.valve_schedule.append([bag_numbers, time_on, time_off])

    def __convert_valve_schedule_to_pump_schedule(self):
        self.pump_schedule = []
        for bag_numbers, time_on, time_off in self.valve_schedule:
            self.pump_schedule.append([bag_numbers, time_on - self.pump_delay, time_off + self.pump_delta])

    @staticmethod
    def read_lines_in_file(file_path):
        with open(file_path) as file:
            lines = file.readlines()
            return lines

    def __iter__(self):
        for item in self.pump_schedule:
            yield item

if __name__ == "__main__":
    schedule = SamplerSchedule("sample.txt")
    for item in schedule:
        print(item)