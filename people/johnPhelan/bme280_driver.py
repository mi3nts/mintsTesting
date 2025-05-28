import smbus2
import bme280
from datetime import datetime, timezone

port    = 5
address = 0x77
bus     = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

data = bme280.sample(bus, address, calibration_params)

"""
Basic print class for the BME280 sensor using the following driver library
https://pypi.org/project/RPi.bme280/#files

Allows the user to print temperature, pressure, or humidity readings
"""
class BME280:
    def print(sensor=None):
        if sensor==None:
            print_all()
        elif sensor == "temperature":
            print(data.temperature)
        elif sensor == "pressure":
            print(data.temperature)
        elif sensor == "humidity":
            print(data.temperature)
        else:
            return "Invalid data type! Please use BME280.print() for all or BME280.print('humidity'), etc"

    def print_all():
        currentTime = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        print("Temperature:", data.temperature)
        print("Pressure:", data.pressure)
        print("Humidity:", data.humidity)

    def sample():
        data = bme280.sample(bus, address, calibration_params)