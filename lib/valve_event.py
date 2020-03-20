"""
Store information about a valve event.
"""

from datetime import datetime

class ValveEvent():
    """
    Class for storing information (time, valve number and action) about a valve event.
    """

    __slots__ = ["valve_time", "valve_number", "valve_action"]

    def __init__(self, time, number, action):
        self.set_valve_time(time)
        self.set_valve_number(number)
        self.set_valve_action(action)

    def set_valve_time(self, time):
        assert(isinstance(time, datetime))
        self.valve_time = time

    def set_valve_number(self, number):
        assert(isinstance(number, int) and number >= 0)
        self.valve_number = number

    def set_valve_action(self, action):
        assert(action == "close valve" or action == "open valve")
        self.valve_action = action

    def get_valve_time(self):
        return self.valve_time

    def get_valve_number(self):
        return self.valve_number

    def get_valve_action(self):
        return self.valve_action

    def get_valve_event(self):
        return (self.valve_time, self.valve_number, self.valve_action)

    def print_valve_event(self):
        print(self.valve_time, "\t", self.valve_number, "\t", self.valve_action)

if __name__ == "__main__":
    current_time = datetime.now().replace(microsecond=0)
    valve_number = 9
    valve_action = "close valve"
    valve = ValveEvent(current_time, valve_number, valve_action)
    valve.print_valve_event()