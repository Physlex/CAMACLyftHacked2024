#!/usr/bin/env python
# Log data from serial port

# Author: Diego Herranz

# Cameron's Nano Port: "/dev/cu.usbserial-14140"

# Run: "python serial_logger.py -d {port}"


import argparse
import serial
import datetime
import time
import os

import numpy as np
import matplotlib.pyplot as plt


fig = plt.figure(figsize = (10, 5))
plt.xlabel("Courses offered")
plt.ylabel("No. of students enrolled")
plt.title("Students enrolled in different courses")

SaveFile = "saves"
CurrentBuffer = ""

# Live plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []




parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-d", "--device", help="device to read from", default="/dev/ttyUSB0")
parser.add_argument("-s", "--speed", help="speed in bps", default=9600, type=int)
args = parser.parse_args()

outputFilePath = os.path.join(os.path.dirname(__file__), SaveFile,
                 datetime.datetime.now().strftime("%Y-%m-%dT%H.%M.%S") + ".bin")

with serial.Serial(args.device, args.speed) as ser, open(outputFilePath, mode='wb') as outputFile:
    print("Logging started. Ctrl-C to stop.") 
    # while True:
    #     try:
    #         data = {'C': np.random.random(), 'C++': np.random.random(), 'Java': np.random.random(), 'Python': np.random.random()}
    #         courses = list(data.keys())
    #         values = list(data.values())
            
    #         plt.clf()
    #         plt.bar(courses, values, color ='maroon', width = 0.4)

    #         ax = plt.gca()
    #         ax.set_ylim([0, 1])
    #         plt.pause(0.05)
        
    #     except KeyboardInterrupt:
    #         print("\n\n== Terminating ==")
    #         break

    try:
        while True:
            # time.sleep(0.1)
            incoming = (ser.read(ser.inWaiting()))
            if(incoming != b''):
                try:
                    CurrentBuffer += incoming.decode("utf-8")
                    outputFile.write(incoming)
                    outputFile.flush()
                except:
                    print("ERROR: Failed to decode bytestring, skipping.")
            if("\n" in CurrentBuffer): # Endline character, ready to flush
                errorString = "ERROR: BUFFER SIZE" + str(len(CurrentBuffer)) + ", FALLING BEHIND" if len(CurrentBuffer) > 500 else ""
                print(errorString + CurrentBuffer.split("\n", 1)[0], )
                CurrentBuffer = CurrentBuffer.split("\n", 1)[1]

                try:
                    data = {'ax': np.random.random(), 'ay': np.random.random(), 'az': np.random.random(), 'gx': np.random.random(), 'gy': np.random.random(), 'gz': np.random.random()}
                    courses = list(data.keys())
                    values = list(data.values())
                    
                    plt.clf()
                    plt.bar(courses, values, color ='maroon', width = 0.4)

                    ax = plt.gca()
                    ax.set_ylim([0, 1])
                    plt.pause(0.05)
                
                except KeyboardInterrupt:
                    print("\n\n== Terminating ==")
                    break

    except KeyboardInterrupt:
        print("Logging stopped")
