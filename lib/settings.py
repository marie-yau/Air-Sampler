# library for board and Broadcom numbering modes
import RPi.GPIO as GPIO

def set_board_numbering_mode(mode):
    """
    Set board numbering mode to either "BCM" (the GPIO is identified by the number that is used by Broadcom, the
    manufacturer) or "BOARD" (the GPIO is identified by the position on the Pi).
    :param mode: String that represents a board numbering mode. Must be either "BCM" or "BOARD".
    """
    assert (mode == "BCM" or mode == "BOARD")
    if mode == "BCM":
        GPIO.setmode(GPIO.BCM)
    elif mode == "BOARD":
        GPIO.setmode(GPIO.BOARD)

def disable_gpio_warnings():
    """
    Disables all GPIO warnings.
    """
    GPIO.setwarnings(False)

def reset_gpio_pins():
    """
    Sets all GPIO pins as output and sets the outputs to False.
    """
    disable_gpio_warnings()
    set_board_numbering_mode("BCM")
    for pin_number in range(0, 28):
        GPIO.setup(pin_number, GPIO.OUT)
        GPIO.output(pin_number, 0)
