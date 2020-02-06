from multiprocessing import Process
from datetime import datetime, timedelta

from sampler_schedule import *
from sampler import *
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

bag_number, valve_time, valve_action = next(valves_schedule)
pump_time, pump_action = next(pump_schedule)

while True:
    current_time = datetime.now().replace(microsecond=0)
    if current_time == pump_time and pump_action == "start pump":
        sampler.turn_pump_on()
        try:
            pump_time, pump_action = next(pump_schedule)
        except:
            pass
    elif current_time == pump_time and pump_action == "stop pump":
        sampler.turn_pump_off()
        try:
            pump_time, pump_action = next(pump_schedule)
        except:
            pass
    elif current_time == valve_time and valve_action == "open valve":
        sampler.open_valve_for_bag(bag_number)
        try:
            bag_number, valve_time, valve_action = next(valves_schedule)
        except:
            pass
    elif current_time == valve_time and valve_action == "close valve":
        sampler.close_valve_for_bag(bag_number)
        try:
            bag_number, valve_time, valve_action = next(valves_schedule)
        except:
            pass