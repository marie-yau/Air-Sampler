def is_valid_GPIO_pin_number(pin_number, mode):
    gpios_in_BCM_mode = [n for n in range(0,28)]
    gpios_in_BOARD_mode =[3,5,7,8,10,11,12,13,15,16,18,19,21,22,23,24,26,27,28,29,31,32,33,35,36,37,38,40]
    if mode == "BCM" and pin_number in gpios_in_BCM_mode:
        return True
    elif mode == "BOARD" and pin_number in gpios_in_BOARD_mode:
        return True
    else:
        return False

#
def is_valid_bag_number(bag_number):
    pass
