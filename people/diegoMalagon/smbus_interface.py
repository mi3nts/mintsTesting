from smbus2 import SMBus
import time

class SMBusSCD30:
    def __init__(self, bus=5, address=0x61):
        self.bus = SMBus(bus)
        self.address = address

    def _crc8(self, data):
        crc = 0xFF
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = ((crc << 1) ^ 0x31) & 0xFF
                else:
                    crc = (crc << 1) & 0xFF
        return crc
      
    def read_words(self, command, count):
        self.write_command(command)
        time.sleep(0.005)

        num_bytes = count * 3  # 2 bytes + 1 CRC per word
        raw = self.bus.read_i2c_block_data(self.address, 0, num_bytes)

    words = []
    for i in range(count):
        msb = raw[i*3]
        lsb = raw[i*3 + 1]
        crc = raw[i*3 + 2]
        if self._crc8([msb, lsb]) != crc:
            raise ValueError("CRC mismatch in word read")
        word = (msb << 8) | lsb
        words.append(word)

    return words


    def write_command(self, command):
        data = [command >> 8, command & 0xFF]
        self.bus.write_i2c_block_data(self.address, 0, data)

    def write_command_with_argument(self, command, argument):
        arg_msb = (argument >> 8) & 0xFF
        arg_lsb = argument & 0xFF
        crc = self._crc8([arg_msb, arg_lsb])
        data = [
            (command >> 8) & 0xFF,
            command & 0xFF,
            arg_msb,
            arg_lsb,
            crc
        ]
        self.bus.write_i2c_block_data(self.address, 0, data)

    def read_register(self, command):
        self.write_command(command)
        time.sleep(0.005)
        raw = self.bus.read_i2c_block_data(self.address, 0, 3)
        msb, lsb, crc = raw
        if self._crc8([msb, lsb]) != crc:
            raise ValueError("CRC mismatch in register read")
        return (msb << 8) | lsb

    def read_measurement(self):
        self.write_command(0x0300)
        time.sleep(0.005)
        raw = self.bus.read_i2c_block_data(self.address, 0, 18)

        def word_to_float(start):
            msb1, lsb1, crc1 = raw[start], raw[start+1], raw[start+2]
            msb2, lsb2, crc2 = raw[start+3], raw[start+4], raw[start+5]
            if self._crc8([msb1, lsb1]) != crc1 or self._crc8([msb2, lsb2]) != crc2:
                raise ValueError("CRC mismatch in float read")
            bytes_ = bytes([msb1, lsb1, msb2, lsb2])
            import struct
            return struct.unpack('>f', bytes_)[0]

        co2 = word_to_float(0)
        temp = word_to_float(6)
        rh = word_to_float(12)
        return co2, temp, rh