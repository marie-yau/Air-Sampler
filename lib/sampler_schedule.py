from datetime import datetime
import re

# TODO: Check file input.

class SamplerSchedule():
    def __init__(self, file_path):
        self.lines_in_file = self.read_lines_in_file(file_path)
        self.__convert_lines_to_schedule()

    def __convert_lines_to_schedule(self):
        self.schedule = []
        # e.g. 1,3; 03/02/19, 11:30:00; 90
        for line in self.lines_in_file:
            line_without_spaces = re.sub(r"\s+", "", line, flags=re.UNICODE)
            bag_numbers, time_on, duration = line_without_spaces.split(";")
            bag_numbers = bag_numbers.split(",")
            bag_numbers = [int(bag_number) for bag_number in bag_numbers]
            time_on = datetime.strptime(time_on, "%m/%d/%y,%H:%M:%S")
            duration = int(duration)
            self.schedule.append([bag_numbers, time_on, duration])

    @staticmethod
    def read_lines_in_file(file_path):
        with open(file_path) as file:
            lines = file.readlines()
            return lines

    def __iter__(self):
        for item in self.schedule:
            yield item

if __name__ == "__main__":
    schedule = SamplerSchedule("sample.txt")
    for item in schedule:
        print(item)