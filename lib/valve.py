import RPi.GPIO as GPIO
import time
import settings
import check

class Valve():
    __slots__ = ["valve_pin_number", "valve_open", "mode"]
    def __init__(self, valve_pin_number, mode):
        # set board numbering mode
        settings.set_board_numbering_mode(mode)
        self.mode = mode
        self.set_valve_pin_number(valve_pin_number)
        self.__valve_set_up()

    def set_valve_pin_number(self, valve_pin_number):
        assert(check.is_valid_GPIO_pin_number(valve_pin_number, self.mode))
        self.valve_pin_number = valve_pin_number

    def __valve_set_up(self):
        GPIO.setup(self.valve_pin_number, GPIO.OUT)
        self.valve_open = False

    # TODO: I am not sure in which position the valve is initially. Should I set the GPIO to 1 or 0 to open the valve?
    def open_valve(self):
        GPIO.output(self.valve_pin_number, 1)
        self.valve_open = True

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