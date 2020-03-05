from multiprocessing import Process
from datetime import datetime, timedelta
import time

from sampler_schedule import *
from sampler import *
from pump_event import *
from configuration import *
from usb_drive import *

def get_current_valve_and_pump_schedules(usb, ID):
    path_to_schedule_file = usb.get_path_for_schedule_file(ID)
    path_to_configuration_file = usb.get_path_for_configuration_file(ID)
    configuration = Configuration(path_to_configuration_file)
    schedules_for_sampler = SamplerSchedule(path_to_schedule_file, configuration.get_pump_starts_before(), configuration.get_pump_stops_after(), configuration.get_pump_time_off_tolerance())
    sampler = Sampler(configuration.get_pump_pin_number(), configuration.get_bag_numbers_to_valve_pin_numbers_dict(), configuration.get_numbering_mode())
    valves_schedule = iter(schedules_for_sampler.get_complete_valve_schedule())
    pump_schedule = iter(schedules_for_sampler.get_complete_pump_schedule())
    return valves_schedule, pump_schedule, sampler

# get ID number from the `.ID.txt` file
path_to_ID_number_file = "/home/pi/.ID.txt"
with open(path_to_ID_number_file, "r") as file:
    content = file.read()
ID_number = int(content)

# wait for USB to be inserted
usb = USB_drive()
while True:
    if usb.is_inserted():
        valves_schedule, pump_schedule, sampler = get_current_valve_and_pump_schedules(usb, ID_number)
        valve_event = next(valves_schedule)
        pump_event = next(pump_schedule)
        break

while True:
    if usb.was_reinserted():
        sampler.turn_pump_off()
        sampler.close_all_valves()
        valves_schedule, pump_schedule, sampler = get_current_valve_and_pump_schedules(usb, ID_number)
        valve_event = next(valves_schedule)
        pump_event = next(pump_schedule)
    current_time = datetime.now().replace(microsecond=0)
    if current_time == pump_event.get_pump_time():
        print(current_time, " pump")
        if pump_event.get_pump_action() == "turn pump on": sampler.turn_pump_on()
        if pump_event.get_pump_action() == "turn pump off": sampler.turn_pump_off()
        try:
            pump_event = next(pump_schedule)
        except StopIteration:
            pass
    if current_time == valve_event.get_valve_time():
        if valve_event.get_valve_action() == "open valve": sampler.open_valve(valve_event.get_valve_number())
        if valve_event.get_valve_action() == "close valve": sampler.close_valve(valve_event.get_valve_number())
        try:
            valve_event = next(valves_schedule)
        except StopIteration:
            pass
    time.sleep(1)