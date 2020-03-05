import RPi.GPIO as GPIO
import settings
import validate
import time
from logger import *

class Pump():
    __slots__ = ["pump_pin_number", "pump_on", "mode"]
    def __init__(self, pump_pin_number, mode):
        # set board numbering mode
        settings.set_board_numbering_mode(mode)
        self.mode = mode
        self.set_pump_pin_number(pump_pin_number)
        self.__pump_setup()

    def set_pump_pin_number(self, pump_pin_number):
        assert(validate.is_valid_GPIO_pin_number(pump_pin_number, self.mode))
        self.pump_pin_number = pump_pin_number

    def __pump_setup(self):
        GPIO.setup(self.pump_pin_number, GPIO.OUT)
        self.pump_on = False

    @event_logger
    def start_pumping(self):
        GPIO.output(self.pump_pin_number, 1)
        self.pump_on = True

    @event_logger
    def stop_pumping(self):
        GPIO.output(self.pump_pin_number, 0)
        self.pump_on = False

    def is_pumping(self):
        return self.pump_on

if __name__ == "__main__":
    pump_pin_number = 27
    numbering_mode = "BCM"
    pump = Pump(pump_pin_number, numbering_mode)
    pump.start_pumping()
    time.sleep(10)
    pump.stop_pumping()