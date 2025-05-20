import time
import board
import busio
import adafruit_scd30

i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
scd = adafruit_scd30.SCD30(i2c)

while True:
    if scd.data_available:
        print("CO2:", scd.CO2, "PPM")
        print("Temperature:", scd.temperature, "°C")
        print("Humidity:", scd.relative_humidity, "%")
        print("")
    time.sleep(2)
