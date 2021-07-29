#lib/seesaw.py

# The MIT License (MIT)
#
# Copyright (c) 2017 Dean Miller for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`seesaw`
====================================================
Based on Adafruit seesaw library
An I2C to whatever helper chip.

* Author: Dean Miller

"""
import time

from machine import I2C
import struct

_STATUS_BASE = const(0x00)

_TOUCH_BASE = const(0x0F)

_STATUS_HW_ID = const(0x01)
_STATUS_TEMP = const(0x04)
_STATUS_SWRST = const(0x7F)

_TOUCH_CHANNEL_OFFSET = const(0x10)

_HW_ID_CODE = const(0x55)

class Seesaw:
    address = 0x36

    def __init__(self, i2c_bus, addr=0x36, drdy=None):
        self._drdy = drdy
        if drdy is not None:
            drdy.switch_to_input()

        self.i2c_device = I2C(i2c_bus, I2C.MASTER)
        address = addr
        print("start scan")
        devices = self.i2c_device.scan()
        for device in devices:
            print("device addr:", device, " hex:", hex(device))
        print("End scan")
        self.sw_reset()

    def sw_reset(self):
        """Trigger a software reset of the SeeSaw chip"""
        self.write8(_STATUS_BASE, _STATUS_SWRST, 0xFF)
        time.sleep(0.500)

        chip_id = self.read8(_STATUS_BASE, _STATUS_HW_ID)

        if chip_id != _HW_ID_CODE:
            raise RuntimeError(
                "Seesaw hardware ID returned (0x{:x}) is not "
                "correct! Expected 0x{:x}. Please check your wiring.".format(
                    chip_id, _HW_ID_CODE
                )
            )

    def moisture_read(self):
        """Read the value of the moisture sensor"""
        buf = bytearray(2)

        self.read(_TOUCH_BASE, _TOUCH_CHANNEL_OFFSET, buf, 0.005)
        ret = struct.unpack(">H", buf)[0]
        time.sleep(0.001)

        # retry if reading was bad
        count = 0
        while ret > 4095:
            self.read(_TOUCH_BASE, _TOUCH_CHANNEL_OFFSET, buf, 0.005)
            ret = struct.unpack(">H", buf)[0]
            time.sleep(0.001)
            count += 1
            if count > 3:
                raise RuntimeError("Could not get a valid moisture reading.")

        return ret

    def get_temp(self):
        """Read the temperature"""
        buf = bytearray(4)
        self.read(_STATUS_BASE, _STATUS_TEMP, buf, 0.005)
        buf[0] = buf[0] & 0x3F
        ret = struct.unpack(">I", buf)[0]
        return 0.00001525878 * ret

    def write8(self, reg_base, reg, value):
        """Write an arbitrary I2C byte register on the device"""
        self.write(reg_base, reg, bytearray([value]))

    def read8(self, reg_base, reg):
        """Read an arbitrary I2C byte register on the device"""
        ret = bytearray(1)
        self.read(reg_base, reg, ret)
        return ret[0]

    def read(self, reg_base, reg, buf, delay=0.008):
        """Read an arbitrary I2C register range on the device"""
        self.write(reg_base, reg)
        if self._drdy is not None:
            while self._drdy.value is False:
                pass
        else:
            time.sleep(delay)

        self.i2c_device.readfrom_into(self.address, buf)

    def write(self, reg_base, reg, buf=None):
        """Write an arbitrary I2C register range on the device"""
        full_buffer = bytearray([reg_base, reg])
        if buf is not None:
            full_buffer += buf

        if self._drdy is not None:
            while self._drdy.value is False:
                pass

        self.i2c_device.writeto(self.address, full_buffer)
