#!/usr/bin/env python3
from time import sleep
import pigpio

class Keypad:
    _cols = [21, 20, 26]
    _rows = [5, 6, 12, 13, 19, 16]

    _keys = [
            ['F','*','CLR'],
            ['E','9','0'],
            ['D','7','8'],
            ['C','5','6'],
            ['B','3','4'],
            ['A','1','2']
        ]
    def __init__(self):
        self._pi = pigpio.pi()

        for col in self._cols:
            self._pi.set_mode(col,pigpio.OUTPUT)
            self._pi.write(col,0)

        for row in self._rows:
            self._pi.set_mode(row,pigpio.INPUT)
            self._pi.set_pull_up_down(row,pigpio.PUD_DOWN)

    def scan(self,blocking=True):
        char = None
        while char is None:
            for col in self._cols:
                self._pi.write(col,1)
                for row in self._rows:
                    state = self._pi.read(row)
                    if state:
                        sleep(0.05)
                        state = self._pi.read(row)
                        if state:
                            char = self._keys[self._rows.index(row)][self._cols.index(col)]
                            #print('(%d,%d): %s'%(row,col,char))
                self._pi.write(col,0)
                sleep(0.05)
            if not blocking:
                break
        return char

    def __del__(self):
        self._pi.stop()

if __name__ == '__main__':
    k = Keypad()
    while True:
        print(k.scan())
