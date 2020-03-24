"""
Package for sampler that contains pump and valves.
"""

import RPi.GPIO as GPIO
import time
import logging

from pump import *
from valve import *

class Sampler():
    """
    Class for setting sampler that contains a pump and valves
    """

    def __init__(self, pump_pin_number, bag_to_valve_pin_numbers_dict, mode, logger):
        self.mode = mode
        self.set_pump(pump_pin_number)
        self.set_valves(bag_to_valve_pin_numbers_dict)
        # TODO: verify that logger is a logging object, not sure how to do that assert(isinstance(logger, ???)
        self.logger = logger

    def set_pump(self, pump_pin_number):
        """
        Sets up a `Pump` objects.
        :param pump_pin_number: Integer that represents a GPIO pin number that the pump is connected to
        """
        self.pump = Pump(pump_pin_number, self.mode, self.logger)

    def set_valves(self, bag_to_valve_pin_numbers_dict):
        """
        Set up `Valve` objects.
        :param bag_to_valve_pin_numbers_dict: Dictionary containing bag numbers (integers) as keys and
        corresponding GPIO numbers (integers) as values.
        :return:
        """
        self.bag_to_valve_objects_dict = {}
        for bag in bag_to_valve_pin_numbers_dict.keys():
            self.bag_to_valve_objects_dict[bag] = Valve(bag_to_valve_pin_numbers_dict[bag], self.mode, self.logger)

    def open_valve(self, bag_number):
        self.bag_to_valve_objects_dict[bag_number].open_valve()

    def close_valve(self, bag_number):
        self.bag_to_valve_objects_dict[bag_number].close_valve()
        
    def close_all_valves(self):
        [valve.close_valve() for valve in self.bag_to_valve_objects_dict.values()]

    def turn_pump_on(self):
        self.pump.start_pumping()

    def turn_pump_off(self):
        self.pump.stop_pumping()


if __name__ == "__main__":
    bags_to_valve_pin_numbers_dict = {1: 17, 2: 22, 3: 10}
    pump_pin_number = 27
    numbering_mode = "BCM"
    sampler = Sampler(pump_pin_number, bags_to_valve_pin_numbers_dict, numbering_mode)
    sampler.open_valve(2)
    sampler.turn_pump_on()
    sampler.open_valve(1)
    time.sleep(10)
    sampler.close_all_valves()
    sampler.turn_pump_off()
