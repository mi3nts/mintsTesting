from scd30_smbus import SCD30
import time

sensor = SCD30(bus=5)

while True:
    if sensor.data_available:
        time.sleep(0.05)  # time to prep the measurement
        try:
            co2, temp, rh = sensor.read_measurement()
            print(f"CO2: {co2:.2f} ppm")
            print(f"Temp: {temp:.2f} °C")
            print(f"Humidity: {rh:.2f} %")
            print()
        except ValueError as e:
            print(f"[ERROR] CRC mismatch while reading measurement: {e}")
    else:
        print("Data not ready yet.")
    time.sleep(2)
