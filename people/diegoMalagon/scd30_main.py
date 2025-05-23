# scd30_main.py

from scd30_smbus import SCD30
import time

sensor = SCD30(bus=5)

while True:
    if sensor.data_available:
        co2, temp, rh = sensor.read_measurement()
        print(f"CO2: {co2:.2f} ppm")
        print(f"Temp: {temp:.2f} °C")
        print(f"Humidity: {rh:.2f} %")
        print()
    time.sleep(0.5)
