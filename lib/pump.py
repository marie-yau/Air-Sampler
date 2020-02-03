import RPi.GPIO as GPIO
import settings
import check
import time

class Pump():
    __slots__ = ["pump_pin_number", "pump_on", "mode"]
    def __init__(self, pump_pin_number, mode):
        # set board numbering mode
        settings.set_board_numbering_mode(mode)
        self.mode = mode
        self.set_pump_pin_number(pump_pin_number)
        self.__pump_set_up()

    def set_pump_pin_number(self, pump_pin_number):
        assert(check.is_valid_GPIO_pin_number(pump_pin_number, self.mode))
        self.pump_pin_number = pump_pin_number

    def __pump_set_up(self):
        GPIO.setup(self.pump_pin_number, GPIO.OUT)
        self.pump_on = False

    def start_pumping(self):
        GPIO.output(self.pump_pin_number, 1)
        self.pump_on = True

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