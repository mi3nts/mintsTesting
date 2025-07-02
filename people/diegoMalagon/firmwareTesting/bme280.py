"""
Basic print class for the BME280 sensor using the following driver library
https://pypi.org/project/RPi.bme280/#files

Allows the user to print temperature, pressure, or humidity readings
"""

import smbus2
import bme280

class BME280:
    def __init__(self, port=5, address=0x77):
        self.port = port
        self.address = address
        self.bus = smbus2.SMBus(self.port)
        self.calibration_params = bme280.load_calibration_params(self.bus, self.address)
        self.data = None

    def sample(self):
        self.data = bme280.sample(self.bus, self.address, self.calibration_params)

    def print(self, sensor=None):
        if self.data is None:
            print("No data available. Run sample() first.")
            return

        if sensor is None:
            self.print_all()
        elif sensor == "temperature":
            print("Temperature:", round(self.data.temperature, 2), "C")
        elif sensor == "pressure":
            print("Pressure:", round(self.data.pressure, 2), "hPa")
        elif sensor == "humidity":
            print("Humidity:", round(self.data.humidity, 2), "%")
        else:
            print("Invalid data type! Use 'temperature', 'pressure', or 'humidity'.")

    def print_all(self):
        print("Temperature:", round(self.data.temperature, 2))
        print("Pressure:", round(self.data.pressure, 2))
        print("Humidity:", round(self.data.humidity, 2))