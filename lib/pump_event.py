"""
Store information (time and action) about a pump event.
"""

from datetime import datetime

class PumpEvent():
    """
    Class for storing information (time and action - either "turn pump on" or "turn pump off") about a pump event.
    """
    __slots__ = ["pump_time", "pump_action"]

    def __init__(self, time, action):
        """
        :param time: `time` object representing the time when the pump action takes place
        :param action: string representing the action of pump, must be either "turn pump on" or "turn pump off"
        """
        self.set_pump_time(time)
        self.set_pump_action(action)

    def set_pump_time(self, time):
        """
        :param time: `time` object representing the time when pump action takes place
        """
        assert(isinstance(time, datetime))
        self.pump_time = time

    def set_pump_action(self, action):
        """
        :param action: string representing the action of pump, must be either "turn pump on" or "turn pump off"
        """
        assert(action == "turn pump on" or action == "turn pump off")
        self.pump_action = action

    def get_pump_time(self):
        """
        :return: `time` object representing the time when pump action takes place
        """
        return self.pump_time

    def get_pump_action(self):
        """
        :return: string representing the action of pump, must be either "turn pump on" or "turn pump off"
        """
        return self.pump_action

    def get_pump_event(self):
        """
        :return: tuple containing:
                    + `time` object representing the time that pump action takes place
                    + String representing the action of pump, must be either "turn pump on" or "turn pump off"
        """
        return (self.pump_time, self.pump_action)

    def print_pump_event(self):
        print(self.pump_time, "\t", self.pump_action)

if __name__ == "__main__":
    current_time = datetime.now().replace(microsecond=0)
    pump_action = "turn pump on"
    pump_event = PumpEvent(current_time, pump_action)
    pump_event.print_pump_event()