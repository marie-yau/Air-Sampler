"""
Store information about sampler schedule.
"""

from datetime import datetime, timedelta
import os
import logging

from pump_event import *
from valve_event import *
from bag_event import *

class SamplerSchedule():
    """
    Class for reading schedule from a text file and generating bag, valve and pump schedules. An example of the required
    format is below.
    The header line ("Bag number, Start filling, Stop filling") has to be exactly in the same format as listed below.
    Line starting with `#` are considered to be comments and are ignored. No blank lines are allowed anywhere in the file.
    Refer to the user_manual.md for more details on file format requirements.
    --------------------------------------------
    Bag number, Start filling, Stop filling
    3,  2020-03-06 11:38:00,  2020-03-06 11:38:30
    1,  2020-03-06 11:38:15,  2020-03-06 11:38:40
    # this is a comment
    2,  2020-03-06 11:39:15,  2020-03-06 11:39:35
    1,  2020-03-06 11:40:00,  2020-03-06 11:40:30
    ---------------------------------------------
    """

    def __init__(self, file_path, pump_start_before, pump_end_after, pump_tolerance, logger, user_logger):
        """
        :param file_path: string representing the path to the schedule file
        :param pump_start_before: `timedelta` object representing the number of seconds that the pump starts pumping
        before the valve opens
        :param pump_end_after: `timedelta` object representing the number of seconds that the pump keeps pumping after
        the valve closes
        :param pump_tolerance: `timedelta` object representing the number of seconds. If pump is supposed to turn off
        for less than specified number of seconds, it will continue pumping.
        :param logger: `logging.Logger` object used for logging actions of the object
        :param user_logger: `logging.Logger` object used for logging invalid format of schedule file
        in a user-friendly way
        """
        self.set_logger(logger)
        self.set_user_logger(user_logger)
        self.set_pump_timedelta_before_valve(pump_start_before)
        self.set_pump_timedelta_after_valve(pump_end_after)
        self.set_pump_off_time_tolerance(pump_tolerance)
        self.file_path = file_path
        self._read_bag_schedule()
        self._create_valve_schedule(self.complete_bag_schedule)
        self._create_pump_schedule(self.complete_bag_schedule)

    def set_logger(self, logger):
        """
        :param logger: `logging.Logger` object used for logging actions of the object
        """
        assert(isinstance(logger, logging.Logger))
        self.logger = logger

    def set_user_logger(self, user_logger):
        assert (isinstance(logger, logging.Logger))
        self.user_logger = user_logger

    def set_pump_timedelta_before_valve(self, pump_start_before):
        """
        :param pump_start_before: `timedelta` object representing the number of seconds that the pump starts pumping
        before the valve opens
        """
        assert(isinstance(pump_start_before, timedelta))
        self.pump_timedelta_before_valve = pump_start_before
        self.logger.info("sampler_schedule.py: set pump to start {} before valve opens".format(self.pump_timedelta_before_valve))

    def set_pump_timedelta_after_valve(self, pump_end_after):
        """
        :param pump_end_after: `timedelta` object representing the number of seconds that the pump keeps pumping after
        the valve closes
        """
        assert (isinstance(pump_end_after, timedelta))
        self.pump_timedelta_after_valve = pump_end_after
        self.logger.info("sampler_schedule.py: set pump to stop {} after valve closes".format(self.pump_timedelta_after_valve))

    def set_pump_off_time_tolerance(self, pump_tolerance):
        """
        :param pump_tolerance: `timedelta` object representing the number of seconds. If pump is supposed to turn off
        for less than specified number of seconds, it will continue pumping.
        """
        assert (isinstance(pump_tolerance, timedelta))
        self.pump_off_time_tolerance = pump_tolerance
        self.logger.info("sampler_schedule.py: set pump time off tolerance to {}".format(self.pump_off_time_tolerance))
        
    def _read_bag_schedule(self):
        """
        Reads bag schedule from file and creates a list of `BagEvent` objects based on the schedule.
        :param user_logger: `logging.Logger` object used for logging invalid format of schedule file
        in a user-friendly way
        """
        assert (isinstance(user_logger, logging.Logger))
        self.complete_bag_schedule = []
        error_messages = []
        try:
            with open(self.file_path) as file:
                # skip header line of file and check its format
                header_line = next(file)
                try:
                    assert(header_line == "Bag number, Start filling, Stop filling\n")
                except:
                    error_messages.append("Line 1: Invalid header. "
                                          "Replace `{}` with `Bag number, Start filling, Stop filling`"
                                          .format(header_line))
                for line_number, line in enumerate(file, 2):
                    # if first character of `line` is `#`, the whole line is considered to be a comment and is skipped
                    if line[0] == "#":
                        continue
                    elif line[0].strip() == "":
                        continue
                    try:
                        bag_event = self.convert_line_to_bag_event(line)
                        self.complete_bag_schedule.append(bag_event)
                    except:
                        error_messages.append("Line {}: Invalid line (`{}`)."
                                              .format(line_number, line))
        except:
            error_messages.append("Schedule file is missing. "
                                  "Create a valid schedule file `{}` on the USB drive. "
                                  .format(self.file_path.split("/")[-1]))

        # sort `self.complete_bag_schedule` by `time_on` in increasing order
        self.complete_bag_schedule.sort(key=lambda event: event.get_bag_time_on())
        # check schedule for overlaps
        for i in range(0, len(self.complete_bag_schedule) - 1):
            if self.complete_bag_schedule[i].get_bag_time_off() > self.complete_bag_schedule[i + 1].get_bag_time_on():
                error_messages.append("Samples in schedule can't overlap. Samples `{}` and `{}` overlap."
                                      .format(self.complete_bag_schedule[i].get_bag_event_as_string(),
                                              self.complete_bag_schedule[i + 1].get_bag_event_as_string()))
        # write error messages to log files
        if error_messages:
            self.user_logger.info("-------------")
            self.logger.info("-------------")
            self.user_logger.info("Schedule file")
            self.logger.info("Schedule file")
            for msg in error_messages:
                self.logger.info(msg)
                self.user_logger.info(msg)
            user_logger.info("\nTo fix `Invalid line` error, check:\n"
                             "- if the line is in the format `<bag number>, <start time>, <stop time>` "
                             "(e.g. `3, 2020-03-06 11:39:15, 2020-03-06 11:39:35`"
                             "- if the bag number is valid (it must be positive integer from interval [1,13])"
                             "- if the times are valid (they must be `YYYY-MM-DD hh:mm:ss` format)"
                             "- if the start time is earlier than stop time")
            self.user_logger.info("-------------")
            self.logger.info("-------------")

            raise ValueError("Schedule file is missing or is in an invalid format.")

        self.logger.info("sampler_schedule.py: read bag schedule from file {}: {}"
                         .format(self.file_path,
                                 [[bag_event.get_bag_number(),
                                   bag_event.get_bag_time_on().strftime("%Y-%m-%d %H:%M:%S"),
                                   bag_event.get_bag_time_off().strftime("%Y-%m-%d %H:%M:%S")]
                                  for bag_event in self.complete_bag_schedule]))

    def _create_valve_schedule(self, bag_schedule):
        """
        Creates a list of `ValveEvent` objects based on `bag_schedule`
        :param bag_schedule: list of `BagEvent` objects
        :return: list of `ValveEvent objects`
        """
        # `bag_schedule` list can't be empty
        assert (len(bag_schedule) > 0)
        valve_schedule = []
        for bag_event in bag_schedule:
            valve_schedule.append(ValveEvent(bag_event.get_bag_time_on(), bag_event.get_bag_number(),  "open valve"))
            valve_schedule.append(ValveEvent(bag_event.get_bag_time_off(), bag_event.get_bag_number(), "close valve"))
        # sort the list according to time
        valve_schedule.sort(key=lambda event: event.get_valve_time())
        return valve_schedule

    def _create_pump_schedule(self, bag_schedule):
        """
        Creates a list of `PumpEvent` objects based on `bag_schedule`.
        :param bag_schedule: list of `BagEvent` objects
        :return: list of `PumpEvent` objects
        """
        # `bag_schedule` list can't be empty
        assert(len(bag_schedule) > 0)
        pump_schedule = []
        # create a list of time intervals when the pump is on, the intervals are in format [time_pump_on, time_pump_off]
        unmerged_pump_on_intervals = [[bag_event.get_bag_time_on() - self.pump_timedelta_before_valve, bag_event.get_bag_time_off()
                                       + self.pump_timedelta_after_valve] for bag_event in bag_schedule]
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
        """
        Creates a list of `BagEvent` objects that contains all `BagEvent` objects created based on the schedule file
        regardless of their starting time.
        :return: list of all `BagEvent` objects from the file
        """
        self._read_bag_schedule()
        self.logger.info("sampler_schedule.py: generated complete bag schedule: {}"
                         .format([[bag_event.get_bag_number(),
                                   bag_event.get_bag_time_on().strftime("%Y-%m-%d %H:%M:%S"),
                                   bag_event.get_bag_time_off().strftime("%Y-%m-%d %H:%M:%S")]
                                  for bag_event in self.complete_bag_schedule]))
        return self.complete_bag_schedule

    def get_complete_valve_schedule(self):
        """
        Creates a list of `ValveEvent` objects that contains all `ValveEvent` objects generated based on the
        `self.complete_bag_schedule`, the complete list of `BagEvent` objects.
        :return: list of all `ValveEvent` objects
        """
        self._read_bag_schedule()
        complete_valve_schedule = self._create_valve_schedule(self.complete_bag_schedule)
        self.logger.info("sampler_schedule.py: generated complete valve schedule: {}"
                         .format([[valve_event.get_valve_number(),
                                   valve_event.get_valve_time().strftime("%Y-%m-%d %H:%M:%S"),
                                   valve_event.get_valve_action()]
                                  for valve_event in complete_valve_schedule]))
        return complete_valve_schedule

    def get_complete_pump_schedule(self):
        """
        Creates a list of `PumpEvent` objects that contains all `PumpEvent` objects generated based on the
        `self.complete_bag_schedule`, the complete list of `BagEvent` objects.
        :return: list of all `PumpEvent` objects
        """
        self._read_bag_schedule()
        complete_pump_schedule = self._create_pump_schedule(self.complete_bag_schedule)
        self.logger.info("sampler_schedule.py: generated complete pump schedule:{}"
                         .format([[pump_event.get_pump_time().strftime("%Y-%m-%d %H:%M:%S"),
                                   pump_event.get_pump_action()]
                                  for pump_event in complete_pump_schedule]))
        return complete_pump_schedule

    def get_current_bag_schedule(self, current_time):
        """
        Creates a list of `BagEvent` objects that contains only objects that have starting time after
        `current_time` + `self.pump_timedelta_before_valve`.
        :param current_time: `datetime` object
        :return: list of `BagEvent` objects with starting time after `current_time` + `self.pump_timedelta_before_valve`
        """
        self._read_bag_schedule()
        current_bag_schedule = []
        for bag_event in self.complete_bag_schedule:
            if bag_event.get_bag_time_on() - self.pump_timedelta_before_valve > current_time:
                current_bag_schedule.append(bag_event)
        self.logger.info("sampler_schedule.py: generated current bag schedule: {}"
                         .format([[bag_event.get_bag_number(),
                                   bag_event.get_bag_time_on().strftime("%Y-%m-%d %H:%M:%S"),
                                   bag_event.get_bag_time_off().strftime("%Y-%m-%d %H:%M:%S")]
                                  for bag_event in current_bag_schedule]))
        return current_bag_schedule

    def get_current_valve_schedule(self, current_time):
        """
        Creates a list of `ValveEvent` objects that contains only objects that have starting time after
        `current_time` + `self.pump_timedelta_before_valve`.
        :param current_time: `datetime` object
        :return: list of `ValveEvent` objects with starting time after `current_time` + `self.pump_timedelta_before_valve`
        """
        self._read_bag_schedule()
        current_bag_schedule = self.get_current_bag_schedule(current_time)
        current_valve_schedule = self._create_valve_schedule(current_bag_schedule)
        self.logger.info("sampler_schedule.py: generated current valve schedule: {}"
                         .format([[valve_event.get_valve_number(),
                                   valve_event.get_valve_time().strftime("%Y-%m-%d %H:%M:%S"),
                                   valve_event.get_valve_action()]
                                  for valve_event in current_valve_schedule]))
        return current_valve_schedule

    def get_current_pump_schedule(self, current_time):
        """
        Creates a list of `PumpEvent` objects that contains only objects that have starting time after `current_time`
        :param current_time: `datetime` object
        :return: list of `PumpEvent` objects with starting time after `current_time`
        """
        self._read_bag_schedule()
        current_bag_schedule = self.get_current_bag_schedule(current_time)
        current_pump_schedule = self._create_pump_schedule(current_bag_schedule)
        self.logger.info("sampler_schedule.py: generated current pump schedule: {}"
                         .format([[pump_event.get_pump_time().strftime("%Y-%m-%d %H:%M:%S"),
                                   pump_event.get_pump_action()]
                                  for pump_event in current_pump_schedule]))
        return current_pump_schedule

    @staticmethod
    def convert_line_to_bag_event(line):
        """
        Converts one line from the schedule file to `BagEvent` object.
        :param line: string representing one line from the schedule file, must be in format
        "3,  2020-03-06 11:38:00,  2020-03-06 11:38:30"
        :return: `BagEvent` object
        """
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
    # create logger
    logging.basicConfig(filename="sampler_schedule.txt",
                        format="%(asctime)s %(message)s",
                        filemode="w",
                        level=logging.DEBUG)
    logger = logging.getLogger()

    file_path = "sample.txt"
    sampler = SamplerSchedule(file_path, timedelta(seconds=5), timedelta(seconds=5), timedelta(seconds=10), logger)

    bag_schedule = sampler.get_complete_bag_schedule()
    print("\nComplete Bag Schedule")
    [event.print_bag_event() for event in bag_schedule]

    valve_schedule = sampler.get_complete_valve_schedule()
    print("\nComplete Valve Schedule")
    [event.print_valve_event() for event in valve_schedule]

    pump_schedule = sampler.get_complete_pump_schedule()
    print("\nComplete Pump Schedule")
    [event.print_pump_event() for event in pump_schedule]

    current_time = datetime(2020, 3, 6, 11, 38, 30)

    bag_schedule = sampler.get_current_bag_schedule(current_time)
    print("\nCurrent Bag Schedule")
    [event.print_bag_event() for event in bag_schedule]

    valve_schedule = sampler.get_current_valve_schedule(current_time)
    print("\nCurrent Valve Schedule")
    [event.print_valve_event() for event in valve_schedule]

    pump_schedule = sampler.get_current_pump_schedule(current_time)
    print("\nCurrent Pump Schedule")
    [event.print_pump_event() for event in pump_schedule]