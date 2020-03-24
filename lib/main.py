from datetime import datetime
import time
import logging
import sys
import threading

from sampler_schedule import *
from sampler import *
from pump_event import *
from configuration import *
from usb_drive import *
from logger import *
from diode import *

def update_schedules_and_configuration(usb, ID, logger):
    """
    Update valve schedule, pump schedule and the configuration of sampler based on its ID number and the files on the
    inserted USB drive.
    :param usb: `USB_drive` object (exactly one USB must be inserted)
    :param ID: Integer that represents the ID number of the sampler
    :return: Iterator over list of `valve_event` objects, iterator over list of `pump_event` objects, `Sampler` object
    """
    path_to_schedule_file = usb.get_path_for_schedule_file(ID)
    path_to_configuration_file = usb.get_path_for_configuration_file(ID)
    # read configuration for sampler from the configuration file
    configuration = Configuration(path_to_configuration_file,
                                  logger)
    # generate valve and pump schedules for sampler based on the schedule file
    schedules_for_sampler = SamplerSchedule(path_to_schedule_file,
                                            configuration.get_pump_starts_before(),
                                            configuration.get_pump_stops_after(),
                                            configuration.get_pump_time_off_tolerance(),
                                            logger)
    # apply configuration to `Sampler` and `Diode` objects
    sampler = Sampler(configuration.get_pump_pin_number(),
                      configuration.get_bag_numbers_to_valve_pin_numbers_dict(),
                      configuration.get_numbering_mode(),
                      logger)
    diode = Diode(configuration.get_diode_pin_number(),
                  configuration.get_numbering_mode(),
                  logger)
    # create iterator over lists of `valve_event` objects and `pump_event` objects
    # note that lists include only future events, not past events
    valves_schedule = iter(schedules_for_sampler.get_current_valve_schedule())
    pump_schedule = iter(schedules_for_sampler.get_current_pump_schedule())
    return valves_schedule, pump_schedule, sampler, diode

# create logger object for logging events and errors
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
logging.basicConfig(filename=current_time + ".log",
                    format="%(asctime)s %(message)s",
                    filemode="w",
                    level=logging.DEBUG)
logger = logging.getLogger()

# handle uncaught exception and safely exit the program
sys.excepthook = log_uncaught_exception

# get ID number of sampler from the `.ID.txt` file
path_to_ID_number_file = "/home/pi/.ID.txt"
with open(path_to_ID_number_file, "r") as file:
    content = file.read()
ID_number = int(content)

# wait for USB to be inserted
usb = USB_drive()
while True:
    if usb.is_inserted():
        valves_schedule, pump_schedule, sampler, diode = update_schedules_and_configuration(usb, ID_number, logger)
        # get next valve and pump event from the iterators
        valve_event = next(valves_schedule)
        pump_event = next(pump_schedule)
        break
    time.sleep(1)

# turn diode on to indicate schedule and configuration file were read correctly
diode_light_thread = threading.Thread(target=diode.turn_diode_on, args=(5,))
diode_light_thread.start()

# this while loop never stops to allow user to reinsert usb with a new schedule even after the current schedule finished
while True:
    # when usb is reinserted, immediately finish the current sample (turn the pump off, close all valves) and update the
    # schedules and configuration
    if usb.was_reinserted():
        sampler.turn_pump_off()
        sampler.close_all_valves()
        valves_schedule, pump_schedule, sampler = update_schedules_and_configuration(usb, ID_number, logger)
        valve_event = next(valves_schedule)
        pump_event = next(pump_schedule)
    # get current time without microseconds
    current_time = datetime.now().replace(microsecond=0)
    if current_time == pump_event.get_pump_time():
        if pump_event.get_pump_action() == "turn pump on":
            sampler.turn_pump_on()
        elif pump_event.get_pump_action() == "turn pump off":
            sampler.turn_pump_off()
        try:
            pump_event = next(pump_schedule)
        except StopIteration:
            pass
    if current_time == valve_event.get_valve_time():
        if valve_event.get_valve_action() == "open valve":
            sampler.open_valve(valve_event.get_valve_number())
        elif valve_event.get_valve_action() == "close valve":
            sampler.close_valve(valve_event.get_valve_number())
        try:
            valve_event = next(valves_schedule)
        except StopIteration:
            pass
    # run the while loop once a second
    time.sleep(1)