from datetime import time

class GeographicPosition():
    __slots__ = ["latitude_degrees", "latitude_direction", "longitude_degrees", "longitude_direction", "time"]

    def __init__(self, lat_degrees, lat_direction, long_degrees, long_direction, position_time):
        self.set_latitude_degrees(lat_degrees)
        self.set_latitude_direction(lat_direction)
        self.set_longitude_degrees(long_degrees)
        self.set_longitude_direction(long_direction)
        self.set_time(position_time)

    def set_latitude_degrees(self, lat_degrees):
        assert(isinstance(lat_degrees, float))
        assert(lat_degrees >= 0 and lat_degrees <= 90)
        self.latitude_degrees = lat_degrees

    def set_latitude_direction(self, lat_direction):
        assert(lat_direction == "N" or lat_direction == "S")
        self.latitude_direction = lat_direction

    def set_longitude_degrees(self, long_degrees):
        assert (isinstance(long_degrees, float))
        assert(long_degrees >= 0 and long_degrees <= 180)
        self.longitude_degrees = long_degrees

    def set_longitude_direction(self, long_direction):
        assert(long_direction == "W" or long_direction == "E")
        self.longitude_direction = long_direction

    def set_time(self, position_time):
        assert(isinstance(position_time, time))
        self.time = position_time

    def get_coordinates(self):
        return self.latitude_degrees, self.latitude_direction, self.longitude_degrees, self.longitude_direction

    def get_time(self):
        return self.time

    def get_coordinates_and_time(self):
        return self.latitude_degrees, self.latitude_direction, self.longitude_degrees, self.longitude_direction, self.time

if __name__ == "__main__":
    position_time = time(13,8,42)
    position = GeographicPosition(43.2542, "N", 123.452, "W", position_time)
    print("Current position coordinates: ", position.get_coordinates())
    print("Position coordinates taken at: ", position.get_time())