#!/usr/bin/env python3
from helper.row_driver import Row
from helper.keypad import Keypad
from helper.display import Display

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
        for row in self.rows:
            self.rows[row].status(False)

        self.keypad = Keypad()
        self.display = Display()

    def get_selection(self):
        while True:
            char = ''
            selection = []
            while True:
                char = self.keypad.scan()
                if char in 'ABCDEF':
                    selection.append(char)
                    self.display.draw_row(char)
                    self.rows[char].status(True)
                    break
            char = self.keypad.scan()
            if char in '123456789':
                selection.append(char)
                self.display.draw_slot(selection[0],selection[1])
                print('Selected %s'%selection)
                return ''.join(selection)
            elif char == 'CLR':
                for row in self.rows:
                    self.rows[row].status(False)
                self.display.splash()
                continue
    
    def vend(self,slot):
        row,col = tuple(slot)
        col = int(col)
        print('Vending from %s,%d'%(row,col))
        self.rows[row].vend(col)
        self.rows[row].status(False)

if __name__ == '__main__':
    vending = Dixie_Narco()
    while True:
        vending.display.splash()
        slot = vending.get_selection()
        vending.vend(slot)
