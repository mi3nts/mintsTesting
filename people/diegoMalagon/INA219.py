from ina219 import INA219, DeviceRangeError
from smbus2 import SMBus
import time

class FirstINA219:
    def __init__(self, address=0x40, bus_num=5):
        self.ina = INA219(0.1, address=address, busnum=bus_num)
        self.ina.configure(self.ina.RANGE_16V)
        self.address = address
        self.bus = SMBus(bus_num)

    def read(self):
        print("Sensor 1:")
        print("  Bus Voltage: %.3f V" % self.ina.voltage())
        try:
            print("  Power: %.3f mW" % self.ina.power())
            print("  Shunt Voltage: %.3f mV" % self.ina.shunt_voltage())
            print("  Bus Current: %.3f mA" % self.ina.current())
        except DeviceRangeError as e:
            print("  Error:", e)


class SecondINA219:
    def __init__(self, address=0x41, bus_num=5):
        self.ina = INA219(0.1, address=address, busnum=bus_num)
        self.ina.configure(self.ina.RANGE_16V)
        self.address = address
        self.bus = SMBus(bus_num)

    def read(self):
        print("Sensor 2:")
        print("  Bus Voltage: %.3f V" % self.ina.voltage())
        try:
            print("  Power: %.3f mW" % self.ina.power())
            print("  Shunt Voltage: %.3f mV" % self.ina.shunt_voltage())
            print("  Bus Current: %.3f mA" % self.ina.current())
        except DeviceRangeError as e:
            print("  Error:", e)





# Continuous loop
if __name__ == "__main__":
    sensor1 = FirstINA219()
    sensor2 = SecondINA219()

    try:
        while True:
            print("\n--- Reading Sensors ---")
            sensor1.read()
            sensor2.read()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nExiting loop.")
