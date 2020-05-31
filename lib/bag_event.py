"""
Store information (bag number, time bag starts filling, time bag stops filling) about a single bag event.
"""

from datetime import datetime, timedelta

class BagEvent():
    """
    Class for storing information (bag number, time bag starts filling, time bag stops filling) about a single bag event.
    """
    __slots__ = ["bag_number", "bag_time_on", "bag_time_off"]

    def __init__(self, bag_number, start_time, end_time):
        """
        :param bag_number: positive integer representing the bag number
        :param start_time: `datetime` object representing the time when the bag starts filling
        :param end_time: `datetime` object representing the time when the bag stops filling
        """
        self.set_bag_number(bag_number)
        self.set_bag_time_on(start_time)
        self.set_bag_time_off(end_time)

    def set_bag_number(self, number):
        """
        :param number: positive integer representing the bag number
        """
        assert(self.is_valid_bag_number(number))
        self.bag_number = number

    def set_bag_time_on(self, time_on):
        """
        Sets `self.bag_time_on` and verifies that it is a `datetime` object and that `self.bag_time_on` is earlier than
        `self.bag_time_off`.
        :param time_on: `datetime` object representing the time when the bag starts filling
        """
        assert(isinstance(time_on, datetime))
        self.bag_time_on = time_on
        # check if `self.bag_time_on` is earlier than `self.bag_time_off`
        try:
            assert(self.bag_time_on < self.bag_time_off)
        # needed in case `self.bag_time_off` hasn't been set yet
        except AttributeError:
            pass

    def set_bag_time_off(self, time_off):
        """
        Sets `self.bag_time_off` and verifies that it is a `datetime` object and that`self.bag_time_on` is earlier than
        `self.bag_time_off`.
        :param time_off: `datetime` object representing the time when the bag stops filling
        """
        assert(isinstance(time_off, datetime))
        self.bag_time_off = time_off
        # check if `self.bag_time_on` is earlier than `self.bag_time_off`
        try:
            assert(self.bag_time_on < self.bag_time_off)
        # needed in case `self.bag_time_on` hasn't been set yet
        except AttributeError:
            pass

    def get_bag_number(self):
        """
        :return: positive integer representing the bag number
        """
        return self.bag_number

    def get_bag_time_on(self):
        """
        :return: `datetime` object representing the time when the bag starts filling
        """
        return self.bag_time_on

    def get_bag_time_off(self):
        """
        :return: `datetime` object that represents the time when the bag stops filling
        """
        return self.bag_time_off

    def get_bag_event(self):
        """
        :return: tuple containing:
                    + positive integer representing the bag number
                    + `datetime` object representing the time when the bag starts filling
                    + `datetime` object that represents the time when the bag stops filling
        """
        return self.bag_number, self.bag_time_on, self.bag_time_off
    
    def get_bag_event_as_string(self):
        return str(self.bag_number) + ", " + self.bag_time_on.strftime("%Y-%m-%d %H:%M:%S") + ", " + self.bag_time_off.strftime("%Y-%m-%d %H:%M:%S") 
    
    def print_bag_event(self):
        """
        Print information contained in the `BagEvent` object.
        """
        print(self.bag_number, "\t", self.bag_time_on, "\t", self.bag_time_off)

    @staticmethod
    def is_valid_bag_number(number):
        """
        :param number: positive integer representing the bag number
        :return: true if `number` is a valid bag number, otherwise false
        """
        if isinstance(number, int) and number > 0 and number < 14:
            return True
        else:
            return False

if __name__ == "__main__":
    bag_number = 5
    start_time = datetime.now().replace(microsecond=0)
    end_time = start_time + timedelta(seconds=90)
    bag = BagEvent(bag_number, start_time, end_time)
    bag.print_bag_event()