"""
Package for GPS module.
"""

import serial
from time import time
from geographic_position import *

class GPS():
    """
    Class for reading the geographic position from GPS module.
    """
    def __init__(self):
        """
        Set the type of sentence that will be read from GPS to GPGGA and the serial port for the GPS.
        GPGGA stands for Global Positioning System Fix Data. An example sentence is $GPGGA,134658.00,5106.9792,N,
        11402.3003,W,2,09,1.0,1048.47,M,-16.27,M,08,AAAA*60" where $GPGGA is a sentence identifier, 134658.00 is time
        (13:46:58 and 00 miliseconds), 5106.9792 is latitude (51 degrees and 06.9792 minutes), N is latitude direction
        (N = North), 11402.3003 is longitude (114 degrees and 02.3003 minutes) and W is longitude direction.
        """
        self._sentence_identifier = "$GPGGA,"
        self._serial_port = serial.Serial("/dev/ttyAMA0")

    def _read_GPS_information(self):
        """
        Reads a geographic position from the GPS module in the NMEA (National Marine Electronics Association) format.
        """
        # continue reading the GPS sentences until a sentence with `self._sentence_identifier` is found.
        while True:
            # read one sentence from the GPS module
            data_from_module = (str)(self._serial_port.readline())
            # the first 7 characters of the sentence contain the sentence identifier.
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
        """
        Reads GPS position in the NMEA format and converts the position to `GeographicPosition` object.
        :return:
        """
        self._read_GPS_information()
        self.latitude_degrees = self.convert_nmea_to_degrees(self._nmea_latitude)
        self.longitude_degrees = self.convert_nmea_to_degrees(self._nmea_longitude)
        self.time = self.convert_nmea_to_time(self._nmea_time[0:6])
        self.position = GeographicPosition(self.latitude_degrees, self.latitude_direction, self.longitude_degrees,
                                           self.longitude_direction, self.time)
        return self.position

    @staticmethod
    def convert_nmea_to_degrees(nmea_value):
        """
        Converts NMEA position format to degrees.
        The NMEA position format is DDmm.mm for latitude and DDDmm.mm for longitude. DD or DDD stands for degrees and
        mm.mm stands for minutes
        :param nmea_value: String representing a position in the NMEA format
        :return: Float that represents the converted values of the NMEA string in degrees
        """
        # verify that `nmea_value` is either string that is convertible to float number or empty string
        assert(nmea_value == "" or nmea_value.replace('.','',1).isdigit())
        try:
            nmea_value = float(nmea_value)
        except ValueError:
            nmea_value = 0
        degrees = int(nmea_value / 100.00)
        minutes = (nmea_value - degrees * 100)
        coordinate_in_degrees = degrees + minutes / 60
        coordinate_in_degrees = round(coordinate_in_degrees, 6)
        assert(coordinate_in_degrees >= 0 and coordinate_in_degrees <= 180)
        return coordinate_in_degrees

    @staticmethod
    def convert_nmea_to_time(nmea_time):
        """
        Converts NMEA time format to `time` object.
        The NMEA time format is HHMMSS.SS where HH is hours, MM is minutes, SS.SS is seconds
        :param nmea_time: String representing a time in the NMEA format
        :return: `time` object that represents the time when the position was taken
        """
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