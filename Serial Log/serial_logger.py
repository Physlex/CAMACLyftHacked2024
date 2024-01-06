#!/usr/bin/env python
# Log data from serial port

# Author: Diego Herranz

# Cameron's Nano Port: "/dev/cu.usbserial-14140"


import argparse
import serial
import datetime
import time
import os

SaveFile = "saves"

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-d", "--device", help="device to read from", default="/dev/ttyUSB0")
parser.add_argument("-s", "--speed", help="speed in bps", default=9600, type=int)
args = parser.parse_args()

outputFilePath = os.path.join(os.path.dirname(__file__), SaveFile,
                 datetime.datetime.now().strftime("%Y-%m-%dT%H.%M.%S") + ".bin")

with serial.Serial(args.device, args.speed) as ser, open(outputFilePath, mode='wb') as outputFile:
    print("Logging started. Ctrl-C to stop.") 
    try:
        while True:
            # time.sleep(1)
            incoming = (ser.read(ser.inWaiting()))
            if(incoming != b''):
                print(incoming)
                outputFile.write(incoming)
                outputFile.flush()
    except KeyboardInterrupt:
        print("Logging stopped")
