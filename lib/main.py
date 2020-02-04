from multiprocessing import Process
from datetime import datetime, timedelta

from sampler_schedule import *
from sampler import *
# hardware set up
bags_to_valve_pin_numbers_dict = {1: 17, 2: 22, 3: 10}
pump_pin_number = 27
mode = "BCM"
# set how many seconds the pump should start pumping before and after the valve opens
pump_delta_seconds = 5
#
pump_tolerance_seconds = 10


# create `file_path` for `file_name` file that is stored in `main.py` file directory
file_name = "sample.txt"
file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "schedules", file_name)

# create `schedule` object that reads sampler's schedule from a file
schedule = SamplerSchedule(file_path, pump_delta_seconds)
# create `sampler` object that operates valves and pump to fill bags
sampler = Sampler(pump_pin_number, bags_to_valve_pin_numbers_dict, mode)

#
processes = []

for bag_numbers, time_on, time_off in schedule:
    # in case the sampler was turned on in the middle of its schedule
    # if `time_on` already passed, skip the current sample
    if datetime.now().replace(microsecond=0) > time_on:
        continue

    try:
        next_bag_number, next_time_on, next_time_off = next(schedule)
        if (next_time_on - time_off) < timedelta(seconds=pump_tolerance_seconds):
            turn_pump_off_after_draw = False
        else:
            turn_pump_off_after_draw = True
    except:
        turn_pump_off_after_draw = True

    while True:
        if datetime.now().replace(microsecond=0) == time_on:
            # fill bags with the same `time_on` and `duration` at the same time
            for bag in bag_numbers:
                process = Process(target=sampler.fill_bag, args=(bag, (time_off - time_on).total_seconds(), pump_delta_seconds, turn_pump_off_after_draw, ))
                processes.append(process)
                process.start()
            # complete the processes
            for proc in processes:
                proc.join()
            processes = []
            break