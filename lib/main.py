from multiprocessing import Process
from datetime import datetime

from sampler_schedule import *
from sampler import *

bags_to_valve_pin_numbers_dict = {1: 17, 2: 22, 3: 10}
pump_pin_number = 27
mode = "BCM"

schedule = SamplerSchedule("sample.txt")
sampler = Sampler(pump_pin_number, bags_to_valve_pin_numbers_dict, mode)

processes = []

for bag_numbers, time_on, duration in schedule:
    while True:
        if datetime.datetime.now().replace(microsecond=0) == time_on:
            for bag in bag_numbers:
                process = Process(target=sampler.fill_bag, args=(bag, duration, ))
                processes.append(process)
                process.start()
            for proc in processes:
                proc.join()
                break