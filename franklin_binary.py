#!/usr/bin/python3

import serial
import sys
import time
import struct
import argparse
import os

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600
    # parity=serial.PARITY_ODD,
    # stopbits=serial.STOPBITS_TWO,
    # bytesize=serial.SEVENBITS
)

parser = argparse.ArgumentParser()
parser.add_argument('file', nargs=1)
parser.add_argument('--raw', action='store_true')
args = parser.parse_args()

dmp = open(args.file[0], 'rb')

if args.raw:
    dmploc = 0x0803
    dmp.seek(0, os.SEEK_END)
    dmplen = dmp.tell()
    dmp.seek(0, os.SEEK_SET)
else:
    dmploc = struct.unpack('<H',dmp.read(2))[0]
    dmplen = struct.unpack('<H',dmp.read(2))[0]
print('Location:',"%02x" % dmploc)
print('Length:',"%02x" % dmplen)

def ace(line):
    for c in line.encode():
        if c != 10:
            c = c | 0x80
            ser.write([c])

ace("CALL -151\r")
time.sleep(1)
bytes_in_line = 1000
for i in range(0,dmplen):
    if bytes_in_line > 8:
        ace("\r")
        sys.stdout.write(str(i*100/dmplen)+"%\r")
        time.sleep(0.25)
        ace(("%04x" % (dmploc + i)) + ":")
        bytes_in_line = 0
    ace(" " + ("%02x" % struct.unpack('B',dmp.read(1))))
    bytes_in_line += 1
ace("\r")
time.sleep(1)
#ace("803G\r")
ace("IN#0\r")
print("\nComplete!")
