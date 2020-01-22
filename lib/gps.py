import time
import serial
import string
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class GPS():
    def __init__(self):
        self._gpgga_info = "$GPGGA,"
        self._ser = serial.Serial("/dev/ttyAMA0")
        self._gpgga_buffer = 0
        self._nmea_buffer = 0


    def get_GPS_nmea_info(self):
        while True:
            data_from_module = (str)(self._ser.readline())
            gpgga_data_from_module = data_from_module.find(self.gpgga_info)
            if gpgga_data_from_module > 0:
                self._gpgga_buffer = data_from_module.split("$GPGGA,", 1)[1]
                nmea_buffer = (self._gpgga_buffer.split(','))
                self._nmea_time = nmea_buffer[0]
                self._nmea_latitude = nmea_buffer[1]
                self._nmea_longitude = nmea_buffer[3]
                self._nmea_latitude, self.nmea_longitude
                break


    def convert_nmea_to_degrees(self):
        nmea_value = float(self._nmea_value)
        decimal_value = nmea_value / 100.00
        degrees = int(decimal_value)
        minutes = (decimal_value - int(decimal_value)) / 60
        position = degrees + minutes
        position = "%.4f" % (position)
        return position


    def get_latitude_and_longitude_in_degrees(self):
        nmea_latitude, nmea_longitude = self.get_GPS_nmea_info()
        degrees_latitude = self.convert_nmea_to_degrees(nmea_latitude)
        degrees_longitude = self.convert_nmea_to_degrees(nmea_longitude)
        return degrees_latitude, degrees_longitude

    def get_time(self):
        self.time_formatted = self._nmea_time[0:2] + ":" + self._nmea_time[2:4] + ":" + self._nmea_time[4:6]
        return self.time_formatted


    def __test__(self):


if __name__ == "__main__":
    gps = GPS()
    GPS.__test__()
