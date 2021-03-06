#!/usr/bin/env python3
from luma.core.interface.serial import spi
from luma.core.render import canvas
from luma.oled.device import ssd1322

from PIL import Image,ImageFont

import signal

class Display:
    def __init__(self):
        self._serial = spi(device=0, port=0, bus_speed_hz=32000000)
        self._device = ssd1322(self._serial,width=256,height=64)
        self._fnt = ImageFont.truetype('/home/agmlego/src/b612/fonts/ttf/B612Mono-Regular.ttf',16)
        signal.signal(signal.SIGALRM,self.handler)

    def handler(self,signum, frame):
        print('Time!')
        with canvas(self._device) as draw:
            draw.rectangle(self._device.bounding_box, outline='black', fill='black')

    def splash(self,slot=''):
        signal.alarm(60)
        with canvas(self._device) as draw:
            draw.rectangle(self._device.bounding_box, outline='white', fill='black')
            draw.text((2,2),'Welcome to i3Detroit!\nPlease make a selection: \n%s'%slot,font=self._fnt,fill='white')
    
    def draw_row(self,row):
        self.splash(row)
    
    def draw_slot(self,row,slot):
        self.splash(row+slot)

if __name__ == '__main__':
    from time import sleep
    disp = Display()
    while True:
        disp.splash()
        row = input('Row? ')
        disp.draw_row(row)
        slot = input('Slot? ')
        disp.draw_slot(row,slot)
        sleep(1)
