from datetime import datetime
import time
import logging
import sys
import threading
import sys
from os.path import join

from sampler_schedule import *
from sampler import *
from pump_event import *
from configuration import *
from usb_drive import *
from logger import *
from diode import *
from settings import *

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

    file_name = str(ID) + "_errors.txt"
    file_path = join(usb.get_path_to_usb(), file_name)
    user_logger = logging.getLogger("user logger")
    user_file_handler = logging.FileHandler(file_path, mode = "w")
    user_logger.addHandler(user_file_handler)
    
    try:
        # read configuration for sampler from the configuration file
        configuration = Configuration(path_to_configuration_file, logger, user_logger)
    except:
        try:
            schedule = SamplerSchedule(path_to_schedule_file, 0, 0, 0, logger, user_logger)
            raise ValueError("Invalid configuration file.")
        except:
            raise ValueError("Invalid configuration file and schedule file.")
    try:
        # generate valve and pump schedules for sampler based on the schedule file
        schedules_for_sampler = SamplerSchedule(path_to_schedule_file,
                                                configuration.get_pump_starts_before(),
                                                configuration.get_pump_stops_after(),
                                                configuration.get_pump_time_off_tolerance(),
                                                logger,
                                                user_logger)
    except:
        raise ValueError("Invalid schedule file.")

    # apply configuration to `Sampler` and `Diode` objects
    sampler = Sampler(configuration.get_pump_pin_number(),
                      configuration.get_bag_numbers_to_valve_pin_numbers_dict(),
                      configuration.get_numbering_mode(),
                      logger)
    diode = Diode(configuration.get_diode_pin_number(),
                  configuration.get_numbering_mode(),
                  logger)
    diode.set_diode_light_duration(configuration.get_diode_light_duration())

    current_time = datetime.now()
    # create iterator over lists of `valve_event` objects and `pump_event` objects
    # note that lists include only future events, not past events
    valves_schedule = iter(schedules_for_sampler.get_current_valve_schedule(current_time))
    pump_schedule = iter(schedules_for_sampler.get_current_pump_schedule(current_time))
    return valves_schedule, pump_schedule, sampler, diode

# create logger object for logging events and errors
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
file_path = "/home/pi/Desktop/sampler_logs/" + current_time + ".log"
logger = logging.getLogger("main logger")
logging.basicConfig(format="%(asctime)s %(message)s",
                    filemode="w",
                    level=logging.DEBUG)
file_handler = logging.FileHandler(file_path)
logger.addHandler(file_handler)

logger.info("main.py: program started")

disable_gpio_warnings()
reset_gpio_pins()

# handle uncaught exception and safely exit the program
sys.excepthook = log_uncaught_exception

# get ID number of sampler from the `.ID.txt` file
path_to_ID_number_file = "/home/pi/.ID.txt"
with open(path_to_ID_number_file, "r") as file:
    content = file.read()
ID_number = int(content)
logger.info("main.py: set ID number of sampler to {}".format(str(ID_number)))

# wait for USB to be inserted
usb = USB_drive(logger)
while True:
    if usb.is_inserted():
        valves_schedule, pump_schedule, sampler, diode = update_schedules_and_configuration(usb, ID_number, logger)
        # get next valve and pump event from the iterators
        try:
            valve_event = next(valves_schedule)
            pump_event = next(pump_schedule)
        except StopIteration:
            logger.error("main.py: no current pump or valve events to execute, exiting the program")
            reset_gpio_pins()
            turn_Pi_off()
        break
    time.sleep(1)

# turn diode on to indicate schedule and configuration file were read correctly
diode_light_thread = threading.Thread(target=diode.turn_diode_on_for, args=(diode.get_diode_light_duration_in_seconds(),))
diode_light_thread.start()

pump_schedule_finished = False
valve_schedule_finished = False
while True:
    # when usb is reinserted, immediately finish the current sample (turn the pump off, close all valves) and update the
    # schedules and configuration
    if usb.was_reinserted():
        sampler.turn_pump_off()
        sampler.close_all_valves()
        valves_schedule, pump_schedule, sampler = update_schedules_and_configuration(usb, ID_number, logger)
        try:
            valve_event = next(valves_schedule)
            pump_event = next(pump_schedule)
        except StopIteration:
            logger.error("main.py: no current pump or valve events to execute, exiting the program")
            reset_gpio_pins()
            turn_Pi_off()
        break
        diode_light_thread = threading.Thread(target=diode.turn_diode_on, args=(diode.get_diode_time_on_in_seconds(),))
        diode_light_thread.start()
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
            pump_schedule_finished = True
            pass
    if current_time == valve_event.get_valve_time():
        if valve_event.get_valve_action() == "open valve":
            sampler.open_valve(valve_event.get_valve_number())
        elif valve_event.get_valve_action() == "close valve":
            sampler.close_valve(valve_event.get_valve_number())
        try:
            valve_event = next(valves_schedule)
        except StopIteration:
            valve_schedule_finished = True
            pass
        
    if valve_schedule_finished and pump_schedule_finished:
        reset_gpio_pins()
        logger.info("main.py: program finished executing the schedule")
        turn_Pi_off()
    # run the while loop once a second
    time.sleep(1)
    