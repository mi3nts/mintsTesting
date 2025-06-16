from smbus2 import SMBus
import time
import struct
from ina219 import INA219
from ina219 import DeviceRangeError


class firstINA219:

    def __init__(self, bus=5, address=0x40):
        self.bus = SMBus(bus)
        self.address = address


    def read():
        ina = INA219(0.1,0x40)
        ina.configure()

        print("Bus Voltage: %.3f V" % ina.voltage())
        try:
            print("Power: %.3f mA" % ina.power())
            print("Shunt Voltage: %.3f mV" % ina.shunt_voltage())
            print('Bus Current: %.3f' % ina.current())


        except DeviceRangeError as e:
            print (e)

class secondINA219:
    def __init__(self, bus=5, address=0x41):
        self.bus = SMBus(bus)
        self.address = address

    def read():
        inaTwo = INA219(0.1,0x41)
        inaTwo.configure()

        print("Bus Voltage: %.3f V" % inaTwo.voltage())
        try:
            print("Power: %.3f mA" % inaTwo.power())
            print("Shunt Voltage: %.3f mV" % inaTwo.shunt_voltage())
            print('Bus Current: %.3f' % inaTwo.current())
            print('Just Voltage: %.3f' & inaTwo.voltage())

        except DeviceRangeError as e:
            print (e)

