#!/usr/bin/env python3
import pigpio

pi = pigpio.pi()

cols = [21, 20, 26]
rows = [5, 6, 12, 13, 19, 20]

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
                print('(%d,%d)'%(row,col))
        pi.write(col,0)

pi.stop()