from time import sleep
from bme280 import BME280  

def main():
    sensor = BME280()

    try:
        while True:
            sensor.sample()
            # print all measurements
            sensor.print()
            print("----------")
            # optionally print individually
            sensor.print("temperature")
            sensor.print("pressure")
            sensor.print("humidity")

            # sample every 5 seconds
            sleep(5)

    except KeyboardInterrupt:
        print("\nExiting program.")

if __name__ == "__main__":
    main()
