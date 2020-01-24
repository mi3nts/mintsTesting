#/dev/ttyUSB0
import csv
import time
import serial
import math
import os
import datetime
from collections import OrderedDict

def split(dataString, dateTime):
    dataOut = dataString.split('@')
    if(len(dataOut) == 2):
        id = dataOut[0]
        sensorData = dataOut[1]
        TSL2591(sensorData, dateTime)

def TSL2591(sensorData, dateTime):
    dataOut = sensorData.split(';')
    length = 4
    if(len(dataOut) == (length + 1)):
        sensorDictionary = OrderedDict([
                ("dateTime", str(dateTime)),
        	    ("Full", dataOut[0]),
            	("Visible", dataOut[1]),
                ("IR", dataOut[2]),
                ("Lux", dataOut[3]),
        	     ])
        csvWriter(sensorDictionary)

def csvWriter(sensorDictionary):
    keys =  list(sensorDictionary.keys())
    exists = os.path.isfile("/home/berkley/Documents/Python3/TSL2591.csv")
    with open('TSL2591.csv', 'a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        if(not(exists)):
            writer.writeheader()
        writer.writerow(sensorDictionary)



ser = serial.Serial('/dev/ttyUSB0')
ser.isOpen()
line = []

while True:
    for x in ser.read():
        line.append(chr(x))
        if chr(x) == '~':
            dataFirst = (''.join(line))
            dataSecond = dataFirst.replace('~', '')
            split(dataSecond, datetime.datetime.now())
            line = []
            break

ser.close()
