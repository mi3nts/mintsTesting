from smbus2 import SMBus
import time

class SMBusSCD30:
    def __init__(self, bus=5, address=0x61):
        self.bus = SMBus(bus)
        self.address = address

    def _crc8(self, data):
        crc = 0xFF  # Initialization value from datasheet
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = ((crc << 1) ^ 0x31) & 0xFF
                else:
                    crc = (crc << 1) & 0xFF
        return crc

    def write_command(self, command, parameters=[]):
        """
        Write a command and optional list of 16-bit words to the sensor with CRC.
        """
        data = []
        for word in parameters:
            msb = (word >> 8) & 0xFF
            lsb = word & 0xFF
            crc = self._crc8([msb, lsb])
            data.extend([msb, lsb, crc])
        self.bus.write_i2c_block_data(self.address, (command >> 8) & 0xFF, [command & 0xFF] + data)

    def read_words(self, command, num_words=3, delay=0.05):
        self.write_command(command)
        time.sleep(delay)
        read_len = num_words * 3
        raw = self.bus.read_i2c_block_data(self.address, 0, read_len)
        words = []
        for i in range(num_words):
            msb, lsb, crc = raw[i*3:i*3+3]
            if crc != self._crc8([msb, lsb]):
                raise ValueError("CRC mismatch")
            words.append((msb << 8) | lsb)
        return words
