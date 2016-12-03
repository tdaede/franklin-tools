#!/usr/bin/python3

import serial
import sys
import time

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600
    # parity=serial.PARITY_ODD,
    # stopbits=serial.STOPBITS_TWO,
    # bytesize=serial.SEVENBITS
)

dmp = open(sys.argv[1], 'rb')

ser.write([13 | 0x80])

for line in dmp:
    print(line)
    line_aced = []
    for c in line:
        if c != 10:
            c = c | 0x80
            ser.write([c])
    time.sleep(1)
