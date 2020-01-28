import RPi.GPIO as GPIO

def set_board_numbering_mode(mode):
    """
    Set board numbering mode to either "BCM" or "BOARD".
    :param mode: String that represents a board numbering mode. Must be either "BCM" or "BOARD".
    """
    assert (mode == "BCM" or mode == "BOARD")
    if mode == "BCM":
        GPIO.setmode(GPIO.BCM)
    elif mode == "BOARD":
        GPIO.setmode(GPIO.BOARD)