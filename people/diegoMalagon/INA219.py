from smbus2 import SMBus
import time
import struct
from ina219 import INA219
from ina219 import DeviceRangeError


class SMBusINA219:
    def __init__(self, bus=5, address=0x40):
        self.bus = SMBus(bus)
        self.address = address


    def read():
        ina = INA219(0.1)
        ina.configure()

        print("Bus Voltage: %.3f V" % ina.bus_voltage())
        try:
            print("Power: %.3f mA" % ina.power())
            print("Shunt Voltage: %.3f mV" % ina.shunt_voltage())
            print('Bus Current: %.3f' % ina.current())
            print('Just Voltage: %3.f' & ina.voltage())

        except DeviceRangeError as e:
            print (e)

