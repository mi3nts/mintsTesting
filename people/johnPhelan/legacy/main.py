#from diegoMalagon.scd30_smbus import SCD30
from johnPhelan.bme280_driver import BME280
from datetime import datetime, timezone
import time

# scd30   = SCD30()
bme280  = BME280()

while True:

    currentTime = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    print("Current time: ", currentTime)

    #scd30 measurements
    # if scd30.data_available:
    #     co2, temp, rh = sensor.read_measurement()
    #     print(f"CO2: {co2:.2f} ppm")
    #     print(f"Temp: {temp:.2f} °C")
    #     print(f"Humidity: {rh:.2f} %")
    #     print()
    
    #BME280 measurements
    try:
        bme280.sample()
        print("BME280 READINGS:")
        bme280.print()
    except Exception as e:
        print("Something went wrong with the BME280 drivers!")

    time.sleep(1)