#!/usr/bin/env python3
import board
import busio
import adafruit_mcp230xx
import digitalio
from time import sleep
i2c = busio.I2C(board.SCL,board.SDA)

rows = []
for addr in range(0x20,0x26):
    try:
        rows.append(adafruit_mcp230xx.MCP23017(i2c,address=addr))
    except (OSError,ValueError):
        print("No such device %x"%addr)
        rows.append(None)

for row in rows:
    if row:
        for pin in range(16):
            row.get_pin(pin).direction = digitalio.Direction.OUTPUT
            row.get_pin(pin).value = False
    
pinmap = {
    'v0':0,
    'v1':1,
    'v2':2,
    'v3':3,
    'v4':4,
    'v5':5,
    'v6':6,
    'v7':7,
    'v8':8,
    'r1':9,
    'r2':10,
    'r3':11,
    'r4':12,
    's':15
}

while True:
    c = input()
    row = rows[int(c[0])]
    if not row:
        print('No such device %s'%c)
        continue
    try:
        pin = pinmap[c[1:]]
        row.get_pin(pin).value = True
        sleep(0.5)
        row.get_pin(pin).value = False
    except KeyError:
        print('bad pin "%s"'%c)
        continue
