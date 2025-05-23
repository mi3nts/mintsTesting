# scd30_smbus.py

from smbus_interface import SMBusSCD30
import struct

CMD_START_CONTINUOUS_MEASUREMENT = 0x0010
CMD_DATA_READY = 0x0202
CMD_READ_MEASUREMENT = 0x0300

class SCD30:
    def __init__(self, bus=5):
        self.i2c = SMBusSCD30(bus)
        self.i2c.write_command(CMD_START_CONTINUOUS_MEASUREMENT, [0])  # ambient pressure = 0

    @property
    def data_available(self):
        result = self.i2c.read_words(CMD_DATA_READY, 1)
        return result[0] == 1

    def read_measurement(self):
        words = self.i2c.read_words(CMD_READ_MEASUREMENT, 6)  # 6 words = 3 floats
        b = bytearray()
        for word in words:
            b.extend(word.to_bytes(2, 'big'))
        co2 = struct.unpack(">f", b[0:4])[0]
        temp = struct.unpack(">f", b[4:8])[0]
        rh = struct.unpack(">f", b[8:12])[0]
        return co2, temp, rh

