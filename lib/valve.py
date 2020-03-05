import RPi.GPIO as GPIO
import time
import settings
import validate
from logger import *

class Valve():
    __slots__ = ["valve_pin_number", "valve_open", "mode"]
    def __init__(self, valve_pin_number, mode):
        # set board numbering mode
        settings.set_board_numbering_mode(mode)
        self.mode = mode
        self.set_valve_pin_number(valve_pin_number)
        self.__valve_setup()

    def set_valve_pin_number(self, valve_pin_number):
        assert(validate.is_valid_GPIO_pin_number(valve_pin_number, self.mode))
        self.valve_pin_number = valve_pin_number

    def __valve_setup(self):
        GPIO.setup(self.valve_pin_number, GPIO.OUT)
        self.valve_open = False

    @event_logger
    def open_valve(self):
        GPIO.output(self.valve_pin_number, 1)
        self.valve_open = True

    @event_logger
    def close_valve(self):
        GPIO.output(self.valve_pin_number, 0)
        self.valve_open = False

    def valve_is_open(self):
        return self.valve_open

if __name__ == "__main__":
    valve_pin_number = 17
    numbering_mode = "BCM"
    valve = Valve(valve_pin_number, numbering_mode)
    valve.open_valve()
    time.sleep(10)
    valve.close_valve()