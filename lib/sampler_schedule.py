from datetime import datetime, timedelta
import re
import os

# TODO: Check file input.

class SamplerSchedule():
    def __init__(self, file_path, pump_start_before, pump_end_after, pump_tolerance):
        self.pump_delta_before = self.convert_seconds_to_timedelta_object(pump_start_before)
        self.pump_delta_after = self.convert_seconds_to_timedelta_object(pump_end_after)
        self.pump_tolerance = self.convert_seconds_to_timedelta_object(pump_tolerance)
        self.file_path = file_path
        self._update_schedule()
        self._create_complete_valve_schedule()
        self._create_complete_pump_schedule()

    def _update_schedule(self):
        self.schedule = []
        with open(self.file_path) as file:
            for line in file:
                line_without_spaces = re.sub(r"\s+", "", line, flags=re.UNICODE)
                bag_info, time_on_info, time_off_info = line_without_spaces.split(";")
                bag_number = int(bag_info)
                time_on = datetime.strptime(time_on_info, "%Y-%m-%d,%H:%M:%S")
                time_off = datetime.strptime(time_off_info, "%Y-%m-%d,%H:%M:%S")
                self.schedule.append([bag_number, time_on, time_off])

    def _create_complete_valve_schedule(self):
        self.complete_valve_schedule = []
        for bag_number, valve_open_at, valve_close_at in self.schedule:
            self.complete_valve_schedule.append([bag_number, valve_open_at, "open valve"])
            self.complete_valve_schedule.append([bag_number, valve_close_at, "close valve"])
        # sort the list according to time
        self.complete_valve_schedule.sort(key=lambda item: item[1])

    def _create_complete_pump_schedule(self):
        self.schedule.sort(key=lambda item: item[1])
        self.complete_pump_schedule = []
        unmerged_pump_on_intervals = [[valve_on - self.pump_delta_before, valve_off + self.pump_delta_after] for bag, valve_on, valve_off in self.schedule]
        unmerged_pump_on_intervals.sort(key=lambda item: item[0])
        merged_pump_on_intervals = [unmerged_pump_on_intervals[0]]
        for current_interval in unmerged_pump_on_intervals:
            previous_interval = merged_pump_on_intervals[-1]
            if current_interval[0] - previous_interval[1] <= self.pump_tolerance:
                previous_interval[1] = max(previous_interval[1], current_interval[1])
            else:
                merged_pump_on_intervals.append(current_interval)

        for interval in merged_pump_on_intervals:
            self.complete_pump_schedule.append([interval[0], "start pump"])
            self.complete_pump_schedule.append([interval[1], "stop pump"])

    def get_complete_valve_schedule(self):
        self._update_schedule()
        self._create_complete_valve_schedule()
        return self.complete_valve_schedule


    def get_complete_pump_schedule(self):
        self._update_schedule()
        self._create_complete_pump_schedule()
        return self.complete_pump_schedule

    def get_current_valve_schedule(self):
        pass

    def get_current_pump_schedule(self):
        pass

    @staticmethod
    def convert_seconds_to_timedelta_object(number_of_seconds):
        delta = timedelta(seconds=number_of_seconds)
        return delta

if __name__ == "__main__":
    file_name = "sample.txt"
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "schedules", file_name)
    sampler = SamplerSchedule(file_path,0,0,0)
    valve_schedule = sampler.get_complete_valve_schedule()
    print("\nValve Schedule")
    for line in valve_schedule:
        print(line)
    pump_schedule = sampler.get_complete_pump_schedule()
    print("\nPump Schedule")
    for line in pump_schedule:
        print(line)