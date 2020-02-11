from datetime import datetime, timedelta

class BagEvent():
    __slots__ = ["bag_number", "bag_time_on", "bag_time_off"]
    def __init__(self, bag_number, start_time, end_time):
        self.set_bag_number(bag_number)
        self.set_bag_time_on(start_time)
        self.set_bag_time_off(end_time)
    
    def set_bag_number(self, number):
        assert(isinstance(number, int) and number >= 0)
        self.bag_number = number
        
    def set_bag_time_on(self, time_on):
        assert(isinstance(time_on, datetime))
        self.bag_time_on = time_on
        
    def set_bag_time_off(self, time_off):
        assert(isinstance(time_off, datetime))
        self.bag_time_off = time_off
        
    def get_bag_number(self):
        return self.bag_number
    
    def get_bag_time_on(self):
        return self.bag_time_on
    
    def get_bag_time_off(self):
        return self.bag_time_off
    
    def get_bag_event(self):
        return (self.bag_number, self.bag_time_on, self.bag_time_off)
    
    def print_bag_event(self):
        print(self.bag_number, "\t", self.bag_time_on, "\t", self.bag_time_off)
        
if __name__ == "__main__":
    bag_number = 5
    start_time = datetime.now().replace(microsecond=0)
    end_time = start_time + timedelta(seconds=90)
    bag = BagEvent(bag_number, start_time, end_time)
    bag.print_bag_event()