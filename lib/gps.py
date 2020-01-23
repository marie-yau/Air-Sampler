import time
import serial
import string
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

class GPS():
    def __init__(self):
        self._gpgga_info = "$GPGGA,"
        self._ser = serial.Serial("/dev/ttyAMA0")
        self.get_current_coordinates()

    def read_GPS_information(self):
        while True:
            data_from_module = (str)(self._ser.readline())
            if data_from_module[0:7] == self._gpgga_info:
                gpgga_buffer = data_from_module.split(self._gpgga_info, 1)[1]
                nmea_buffer = (gpgga_buffer.split(','))
                self._nmea_time = nmea_buffer[0]
                self._nmea_latitude = nmea_buffer[1]
                self.latitude_direction = nmea_buffer[2]
                self._nmea_longitude = nmea_buffer[3]
		        self.longitude_direction = nmea_buffer[4]
		        break

    def _convert_nmea_to_degrees(self, nmea_value):
        try:
            nmea_value = float(nmea_value)
        except(TypeError, ValueError):
            nmea_value = 0
        decimal_value = nmea_value / 100.00
        degrees = int(decimal_value)
        minutes = (decimal_value - int(decimal_value)) / 60
        position = degrees + minutes
        position = "%.4f" % (position)
        return position

    def get_coordinates(self):
        self.latitude_degrees = self._convert_nmea_to_degrees(self._nmea_latitude)
        self.longitude_degrees = self._convert_nmea_to_degrees(self._nmea_longitude)
        return self.latitude_degrees, self.latitude_direction, self.longitude_degrees, self.longitude_direction

    def get_time(self):
        self.time = self._nmea_time[0:2] + ":" + self._nmea_time[2:4] + ":" + self._nmea_time[4:6]
        return self.time

    def print_coordinates_and_time(self):
        print("Time: ", self.time)
        print("Latitude: ", self.latitude_degrees, " ", self.latitude_direction)
        print("Longitude: ", self.longitude_degrees, " ", self.longitude_direction)

if __name__ == "__main__":
    myGPS = GPS()
    myGPS.read_GPS_information()
    myGPS.print_coordinates_and_time()