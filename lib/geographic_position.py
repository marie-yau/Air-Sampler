"""
Store geographic position as longitude and latitude at the given time.
"""

from datetime import time

class GeographicPosition():
    """
    Class for storing the geographic position as longitude and latitude at the given time.
    """
    __slots__ = ["latitude_degrees", "latitude_direction", "longitude_degrees", "longitude_direction", "time"]

    def __init__(self, lat_degrees, lat_direction, long_degrees, long_direction, position_time):
        self.set_latitude_degrees(lat_degrees)
        self.set_latitude_direction(lat_direction)
        self.set_longitude_degrees(long_degrees)
        self.set_longitude_direction(long_direction)
        self.set_time(position_time)

    def set_latitude_degrees(self, lat_degrees):
        """
        :param lat_degrees: Float representing latitude in degrees where degrees are between 0 and 90.
        """
        assert(isinstance(lat_degrees, float))
        assert(lat_degrees >= 0 and lat_degrees <= 90)
        self.latitude_degrees = lat_degrees

    def set_latitude_direction(self, lat_direction):
        """
        :param lat_direction: Float representing latitude direction, must be either "N" or "S"
        """
        assert(lat_direction == "N" or lat_direction == "S")
        self.latitude_direction = lat_direction

    def set_longitude_degrees(self, long_degrees):
        """
        :param long_degrees: Float representing longitude in degrees where degrees are between 0 and 90
        """
        assert (isinstance(long_degrees, float))
        assert(long_degrees >= 0 and long_degrees <= 180)
        self.longitude_degrees = long_degrees

    def set_longitude_direction(self, long_direction):
        """
        :param long_direction: Float representing latitude direction, must be either "W" or "E"
        """
        assert(long_direction == "W" or long_direction == "E")
        self.longitude_direction = long_direction

    def set_time(self, position_time):
        """
        :param position_time: `datetime` object representing the time when the geographic position was taken
        """
        assert(isinstance(position_time, time))
        self.time = position_time

    def get_coordinates(self):
        """
        :return: tuple containing
                    + Float that represents latitude in degrees where degrees are between 0 and 90
                    + Float that represents latitude direction, must be either "N" or "S"
                    + Float that represents longitude in degrees where degrees are between 0 and 90
                    + Float that represents latitude direction, must be either "W" or "E"
        """
        return self.latitude_degrees, self.latitude_direction, self.longitude_degrees, self.longitude_direction

    def get_time(self):
        """
        :return: `datetime` object that represents the time when the geographic position was taken
        """
        return self.time

    def get_coordinates_and_time(self):
        """
        :return: tuple containing
                    + Float that represents latitude in degrees where degrees are between 0 and 90
                    + Float that represents latitude direction, must be either "N" or "S"
                    + Float that represents longitude in degrees where degrees are between 0 and 90
                    + Float that represents latitude direction, must be either "W" or "E"
                    + `datetime` object that represents the time when the geographic position was taken
        """
        return self.latitude_degrees, self.latitude_direction, self.longitude_degrees, self.longitude_direction, self.time

if __name__ == "__main__":
    position_time = time(13,8,42)
    position = GeographicPosition(43.2542, "N", 123.452, "W", position_time)
    print("Current position coordinates: ", position.get_coordinates())
    print("Position coordinates taken at: ", position.get_time())