from multiprocessing import Process
from datetime import datetime, timedelta

from sampler_schedule import *
from sampler import *
from valve_event import *
from pump_event import *

# hardware set up
bags_to_valve_pin_numbers_dict = {1: 17, 2: 22, 3: 10}
pump_pin_number = 27
mode = "BCM"
# set how many seconds the pump should start pumping before and after the valve opens
pump_starts_before = 5
pump_ends_after = 5
pump_tolerance_seconds = 10


# create `file_path` for `file_name` file that is stored in `main.py` file directory
path = os.getcwd()
file_path = os.path.abspath(os.path.join(path, os.pardir, "schedules", "sample.txt"))
# create `schedule` object that reads sampler's schedule from a file
schedules_for_sampler = SamplerSchedule(file_path, pump_starts_before, pump_ends_after, pump_tolerance_seconds)
# create `sampler` object that operates valves and pump to fill bags
sampler = Sampler(pump_pin_number, bags_to_valve_pin_numbers_dict, mode)

valves_schedule = iter(schedules_for_sampler.get_complete_valve_schedule())
pump_schedule = iter(schedules_for_sampler.get_complete_pump_schedule())

valve_event = next(valves_schedule)
pump_event = next(pump_schedule)


while True:
    current_time = datetime.now().replace(microsecond=0)
    if current_time == pump_event.get_pump_time():
        if pump_event.get_pump_action() == "turn pump on": sampler.turn_pump_on()
        if pump_event.get_pump_action() == "turn pump off": sampler.turn_pump_off()
        try:
            pump_event = next(pump_schedule)
        except StopIteration:
            pass
    if current_time == valve_event.get_valve_time():
        if valve_event.get_valve_action() == "open valve": sampler.open_valve_for_bag()
        if valve_event.get_valve_action() == "close valve": sampler.close_valve_for_bag()
        try:
            valve_event = next(valves_schedule)
        except StopIteration:
            pass
