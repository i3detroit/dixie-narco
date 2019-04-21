#!/usr/bin/env python3
from time import sleep
import pigpio

pi = pigpio.pi()

cols = [21, 20, 26]
rows = [5, 6, 12, 13, 19, 16]

keys = [
        ['F','*','CLR'],
        ['E','9','0'],
        ['D','7','8'],
        ['C','5','6'],
        ['B','3','4'],
        ['A','1','2']
     ]

for col in cols:
    pi.set_mode(col,pigpio.OUTPUT)
    pi.write(col,0)

for row in rows:
    pi.set_mode(row,pigpio.INPUT)
    pi.set_pull_up_down(row,pigpio.PUD_DOWN)
    pi.set_glitch_filter(row,100)

while True:
    for col in cols:
        pi.write(col,1)
        for row in rows:
            state = pi.read(row)
            if state:
                sleep(0.2)
                state = pi.read(row)
                if state:
                    char = keys[rows.index(row)][cols.index(col)]
                    print('(%d,%d): %s'%(row,col,char))
        pi.write(col,0)
        sleep(0.05)

pi.stop()
