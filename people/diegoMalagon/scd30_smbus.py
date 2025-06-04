# scd30_smbus.py

from smbus_interface import SMBusSCD30
import struct

CMD_START_CONTINUOUS_MEASUREMENT = 0x0010
CMD_STOP_CONTINUOUS_MEASUREMENT = 0x0104
CMD_SET_INTERVAL = 0x4600 #initial value is 2 seconds
CMD_DATA_READY = 0x0202
CMD_READ_MEASUREMENT = 0x0300
CMD_TEMP_OFFSET = 0x5403 # argument needed
CMD_ALT_COMP = 0x5102 # argument
CMD_SET_FRC = 0x5204 #argument neeeded

class SCD30:
    def __init__(self, bus=5):
        self.i2c = SMBusSCD30(bus)
        self.i2c.write_command_with_argument(CMD_START_CONTINUOUS_MEASUREMENT, 0)  # ambient pressure = 0

    @property
    def data_available(self):
        result = self.i2c.read_words(CMD_DATA_READY, 1)
        return result[0] == 1

    def read_measurement(self):
        raw_words = self.i2c.read_words(CMD_READ_MEASUREMENT, 6)  # 6 words = 3 floats

        co2  = word_to_float(raw_words[0], raw_words[1])
        temp = word_to_float(raw_words[2], raw_words[3])
        humid  = word_to_float(raw_words[4], raw_words[5])

        return co2, temp, humid