#!/usr/bin/env python3
import board
import busio
import adafruit_mcp230xx
import digitalio
from time import sleep

class I2C:
    _shared_state = {}
    def __init__(self):
        self.__dict__ = self._shared_state
        self.i2c = busio.I2C(board.SCL,board.SDA)
    def __hash__(self): return 1
    def __eq__(self, other):
        try: return self.__dict__ is other.__dict__
        except: return 0

class Row:
    _pinmap = (None,8,7,6,5,4,3,2,1,0)
    _status = 15
    def __init__(self,address=0x20,label='F'):
        self._i2c = I2C()
        self.address = address
        self.label = label
        try:
            self._driver = adafruit_mcp230xx.MCP23017(self._i2c.i2c,address=self.address)
            for pin in self._pinmap[1:]+(self._status):
                self._driver.get_pin(pin).direction = digitalio.Direction.OUTPUT
                self._driver.get_pin(pin).value = False
            self.status(True)
        except (OSError,ValueError):
            print("No such device %x"%self.address)
            raise

    def vend(self,slot):
        pin = self._pinmap[slot]
        self._driver.get_pin(pin).value = True
        sleep(0.5)
        self._driver.get_pin(pin).value = False

    def status(self,state):
        self._driver.get_pin(self._status).value = state

if __name__ == '__main__':
    rows = {
        'A':Row(0x25,'A'),
        'B':Row(0x24,'B'),
        'C':Row(0x23,'C'),
        'D':Row(0x22,'D'),
        'E':Row(0x21,'E'),
        'F':Row(0x20,'F')
    }

    while True:
        c = input()
        row = rows[c[0]]
        if not row:
            print('No such device %s'%c)
            continue
        try:
            row.vend(int(c[1]))
        except (IndexError,AttributeError):
            print('bad pin "%s"'%c)
            continue
