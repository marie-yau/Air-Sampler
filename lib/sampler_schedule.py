"""
Store information about sampler schedule.
"""

from datetime import datetime, timedelta
import os

from pump_event import *
from valve_event import *
from bag_event import *

class SamplerSchedule():

    def __init__(self, file_path, pump_start_before, pump_end_after, pump_tolerance, logger):
        self.pump_timedelta_before_valve = pump_start_before
        self.pump_timedelta_after_valve = pump_end_after
        self.pump_off_time_tolerance = pump_tolerance
        self.file_path = file_path
        self._read_bag_schedule()
        self._create_valve_schedule(self.complete_bag_schedule)
        self._create_pump_schedule(self.complete_bag_schedule)
        # TODO: verify that logger is a logging object, not sure how to do that assert(isinstance(logger, ???)
        self.logger = logger
        
    def _read_bag_schedule(self):
        self.complete_bag_schedule = []
        with open(self.file_path) as file:
            # skip header line of file and check its format
            header_line = next(file)
            assert(header_line == "Bag number, Start filling, Stop filling\n")
            for line in file:
                # if first character of `line` is `#`, the whole line is considered to be a comment and is skipped
                if line[0] == "#":
                    continue
                bag_event = self.convert_line_to_bag_event(line)
                self.complete_bag_schedule.append(bag_event)
        # sort `self.complete_bag_schedule` by `time_on` in increasing order
        self.complete_bag_schedule.sort(key=lambda event: event.get_bag_time_on())

    def _create_valve_schedule(self, bag_schedule):
        valve_schedule = []
        for bag_event in bag_schedule:
            valve_schedule.append(ValveEvent(bag_event.get_bag_time_on(), bag_event.get_bag_number(),  "open valve"))
            valve_schedule.append(ValveEvent(bag_event.get_bag_time_off(), bag_event.get_bag_number(), "close valve"))
        # sort the list according to time
        valve_schedule.sort(key=lambda event: event.get_valve_time())
        return valve_schedule

    def _create_pump_schedule(self, bag_schedule):
        pump_schedule = []
        # create a list of time intervals when the pump is on, the intervals are in format [time_pump_on, time_pump_off]
        unmerged_pump_on_intervals = [[bag_event.get_bag_time_on() - self.pump_timedelta_before_valve, bag_event.get_bag_time_off() + self.pump_timedelta_after_valve]
                                      for bag_event in bag_schedule]
        # sort the list of time intervals by the time pump turns on
        unmerged_pump_on_intervals.sort(key=lambda interval: interval[0])

        # merge all time intervals that overlap or the difference between one interval's time off and the another
        # interval's time on is less or equal to `self.pump_off_time_tolerance`
        merged_pump_on_intervals = [unmerged_pump_on_intervals[0]]
        for current_interval in unmerged_pump_on_intervals:
            previous_interval = merged_pump_on_intervals[-1]
            if current_interval[0] - previous_interval[1] <= self.pump_off_time_tolerance:
                previous_interval[1] = max(previous_interval[1], current_interval[1])
            else:
                merged_pump_on_intervals.append(current_interval)
        # create schedule for pump
        for interval in merged_pump_on_intervals:
            pump_schedule.append(PumpEvent(interval[0], "turn pump on"))
            pump_schedule.append(PumpEvent(interval[1], "turn pump off"))
        return pump_schedule

    def get_complete_bag_schedule(self):
        return self.complete_bag_schedule

    def get_complete_valve_schedule(self):
        self._read_bag_schedule()
        complete_valve_schedule = self._create_valve_schedule(self.complete_bag_schedule)
        return complete_valve_schedule

    def get_complete_pump_schedule(self):
        self._read_bag_schedule()
        complete_pump_schedule = self._create_pump_schedule(self.complete_bag_schedule)
        return complete_pump_schedule

    def get_current_bag_schedule(self, current_time):
        self._read_bag_schedule()
        current_bag_schedule = []
        self.logger.info("Sampler schedule: generating current bag schedule:")
        for bag_event in self.complete_bag_schedule:
            if bag_event.get_bag_time_on() - self.pump_timedelta_before_valve > current_time:
                current_bag_schedule.append(bag_event)
                #self.logger.info("Sampler schedule: {}, {}, {}".format(bag_event.get_bag_event())
        return current_bag_schedule

    def get_current_valve_schedule(self, current_time):
        self._read_bag_schedule()
        current_bag_schedule = self.get_current_bag_schedule(current_time)
        current_valve_schedule = self._create_valve_schedule(current_bag_schedule)
        self.logger.info("Generated current valve schedule:\n{}".format(current_valve_schedule))
        return current_valve_schedule

    def get_current_pump_schedule(self, current_time):
        self._read_bag_schedule()
        current_bag_schedule = self.get_current_bag_schedule(current_time)
        current_pump_schedule = self._create_pump_schedule(current_bag_schedule)
        self.logger.info("Generated current pump schedule:\n{}".format(current_pump_schedule))
        return current_pump_schedule

    @staticmethod
    def convert_line_to_bag_event(line):
        bag_info, time_on_info, time_off_info, *rest = line.split(",")
        # check if line contains only three values
        assert(not rest)
        # convert `bag_info` to integer
        bag_number = int(bag_info.strip())
        # convert `time_on_info` to datetime object
        time_on_info = " ".join(time_on_info.strip().split())
        time_off_info = " ".join(time_off_info.strip().split())
        time_on = datetime.strptime(time_on_info, "%Y-%m-%d %H:%M:%S")
        time_off = datetime.strptime(time_off_info, "%Y-%m-%d %H:%M:%S")
        # check if `time_on` is earlier than `time_off`
        assert(time_on < time_off)
        return BagEvent(bag_number, time_on, time_off)

if __name__ == "__main__":
    file_name = "sample.txt"
    file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "schedules", file_name)
    sampler = SamplerSchedule(file_path,5,5,10)
    bag_schedule = sampler.get_complete_bag_schedule()
    print("\nBag Schedule")
    for event in bag_schedule:
        event.print_bag_event()
    valve_schedule = sampler.get_complete_valve_schedule()
    print("\nValve Schedule")
    for event in valve_schedule:
        event.print_valve_event()
    pump_schedule = sampler.get_complete_pump_schedule()
    print("\nPump Schedule")
    for event in pump_schedule:
        event.print_pump_event()