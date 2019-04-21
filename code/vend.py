#!/usr/bin/env python3
from helper.row_driver import Row
from helper.keypad import Keypad

class Dixie_Narco:
    def __init__(self):
        self.rows = {
            'A':Row(0x25,'A'),
            'B':Row(0x24,'B'),
            'C':Row(0x23,'C'),
            'D':Row(0x22,'D'),
            'E':Row(0x21,'E'),
            'F':Row(0x20,'F')
        }

        self.keypad = Keypad()

    def get_selection(self):
        while True:
            char = None
            selection = ''
            while char not in 'ABCDEF':
                char = self.keypad.scan()
            selection += char
            char = self.keypad.scan()
            if char in '123456789':
                selection += char
                print('Selected %s'%selection)
                return selection
            elif char == 'CLR':
                continue
    
    def vend(self,slot):
        row,col = tuple(slot)
        col = int(col)
        print('Vending from %s,%d'%(row,col))
        self.rows[row].vend(col)

if __name__ == '__main__':
    vending = Dixie_Narco()
    while True:
        slot = vending.get_selection()
        vending.vend(slot)