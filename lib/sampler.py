import RPi.GPIO as GPIO
import time
from pump import *
from valve import *

class Sampler():
    def __init__(self, pump_pin_number, bag_to_valve_pin_numbers_dict, mode):
        self.mode = mode
        self.set_pump(pump_pin_number)
        self.set_valves(bag_to_valve_pin_numbers_dict)

    def set_pump(self, pump_pin_number):
        self.pump = Pump(pump_pin_number, self.mode)

    def set_valves(self, bag_to_valve_pin_numbers_dict):
        self.bag_to_valve_objects_dict = {}
        for bag in bag_to_valve_pin_numbers_dict.keys():
            self.bag_to_valve_objects_dict[bag] = Valve(bag_to_valve_pin_numbers_dict[bag], self.mode)

    def fill_bag(self, bag_number, duration):
        self.pump.start_pumping()
        self.bag_to_valve_objects_dict[bag_number].open_valve()
        time.sleep(duration)
        self.bag_to_valve_objects_dict[bag_number].close_valve()
        self.pump.stop_pumping()

if __name__ == "__main__":
    bags_to_valve_pin_numbers_dict = {1: 17, 2: 22, 3: 10}
    pump_pin_number = 27
    numbering_mode = "BCM"
    sampler = Sampler(pump_pin_number, bags_to_valve_pin_numbers_dict, numbering_mode)
    sampler.fill_bag(2, 15)
    time.sleep(20)
    sampler.fill_bag(1, 30)