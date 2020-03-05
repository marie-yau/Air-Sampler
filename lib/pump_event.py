from datetime import datetime

class PumpEvent():
    __slots__ = ["pump_time", "pump_action"]
    def __init__(self, time, action):
        self.set_pump_time(time)
        self.set_pump_action(action)

    def set_pump_time(self, time):
        assert(isinstance(time, datetime))
        self.pump_time = time

    def set_pump_action(self, action):
        assert(action == "turn pump on" or action == "turn pump off")
        self.pump_action = action

    def get_pump_time(self):
        return self.pump_time

    def get_pump_action(self):
        return self.pump_action

    def get_pump_event(self):
        return (self.pump_time, self.pump_action)

    def print_pump_event(self):
        print(self.pump_time, "\t", self.pump_action)

if __name__ == "__main__":
    current_time = datetime.now().replace(microsecond=0)
    pump_action = "turn pump on"
    pump_event = PumpEvent(current_time, pump_action)
    pump_event.print_pump_event()