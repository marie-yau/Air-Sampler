"""
Package for GPS module.
"""
import serial
from geographic_position import *

class GPS():
    def __init__(self):
        self._sentence_identifier = "$GPGGA,"
        self._ser = serial.Serial("/dev/ttyAMA0")

    def _read_GPS_information(self):
        while True:
            data_from_module = (str)(self._ser.readline())
            if data_from_module[0:7] == self._sentence_identifier:
                gpgga_buffer = data_from_module.split(self._sentence_identifier, 1)[1]
                nmea_buffer = (gpgga_buffer.split(','))
                self._nmea_time = nmea_buffer[0]
                self._nmea_latitude = nmea_buffer[1]
                self.latitude_direction = nmea_buffer[2]
                self._nmea_longitude = nmea_buffer[3]
                self.longitude_direction = nmea_buffer[4]
                break

    def get_geographic_position(self):
        self._read_GPS_information()
        self.latitude_degrees = self.convert_nmea_to_degrees(self._nmea_latitude)
        self.longitude_degrees = self.convert_nmea_to_degrees(self._nmea_longitude)
        self.time = self.convert_nmea_to_time(self._nmea_time[0:6])
        self.position = GeographicPosition(self.latitude_degrees, self.latitude_direction, self.longitude_degrees, self.longitude_direction, self.time)
        return self.position

    @staticmethod
    def convert_nmea_to_degrees(nmea_value):
        # TODO: `nmea_value` must be either string that is convertable to float number or empty string. Test if `nmea_value` satisfies those conditions.
        try:
            nmea_value = float(nmea_value)
        except(TypeError, ValueError):
            nmea_value = 0
        degrees = int(nmea_value / 100.00)
        minutes = (nmea_value - degrees * 100)
        coordinate_in_degrees = degrees + minutes / 60
        coordinate_in_degrees = round(coordinate_in_degrees, 6)
        return coordinate_in_degrees

    @staticmethod
    def convert_nmea_to_time(nmea_time):
        assert(len(nmea_time) == 6)
        assert(isinstance(nmea_time, str) and nmea_time.isdigit())
        hours = int(nmea_time[0:2])
        minutes = int(nmea_time[2:4])
        seconds = int(nmea_time[4:6])
        return time(hours, minutes, seconds)

if __name__ == "__main__":
    myGPS = GPS()
    current_position = myGPS.get_geographic_position()
    print("Coordinates: ", current_position.get_coordinates())
    print("Time: ", current_position.get_time())