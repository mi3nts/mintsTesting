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

        # Optional: print raw register data
        self.read_raw_registers()

    def read_raw_registers(self):
        print("  Raw I2C Register Data:")
        for reg in range(0x00, 0x06):  # 0x00 to 0x05 are the main INA219 registers
            value = self.bus.read_word_data(self.address, reg)
            swapped = ((value << 8) & 0xFF00) | (value >> 8)  # convert from little-endian
            print(f"    Reg 0x{reg:02X}: 0x{swapped:04X}")

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

        self.read_raw_registers()

    def read_raw_registers(self):
        print("  Raw I2C Register Data:")
        for reg in range(0x00, 0x06):
            value = self.bus.read_word_data(self.address, reg)
            swapped = ((value << 8) & 0xFF00) | (value >> 8)
            print(f"    Reg 0x{reg:02X}: 0x{swapped:04X}")


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
