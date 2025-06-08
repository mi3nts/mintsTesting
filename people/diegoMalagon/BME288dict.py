from collections import OrderedDict
from datetime import datetime, timezone
import time
import os
import sys
import glob
import serial
import csv


port = '/dev/tty.usbserial-110'
ser = serial.Serial(port = port, baudrate = 115200, timeout = 1)

csv_file = 'canareeData.csv'

bme688_keys = ['Temperature', 'Humidity', 'Pressure', ' Gas']
ips7100_keys = ['PM0.1', 'PM0.3', 'PM0.5', 'PM1', 'PM2.5', 'PM5', 'PM10']
all_keys = ['timestamp'] + bme688_keys + ips7100_keys

if not os.path.isfile(csv_file):
    with open(csv_file, mode = 'w', newline = '') as f:
        write = csv.DictWriter(f, fieldnames = all_keys)
        write.writeheader()

def read_sensor():
    try:
        line = ser.readline().decode('utf-8').strip()
        print("RAW SENSOR DATA: ",  line)
        return line
    except serial.SerialException as e:
        print('SERIAL ERROR: ', {e})
        return None
    
def parse_data(raw_data):

    currentTime = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    try:
        parts = raw_data.split(',')
        data_dict = dict(zip(parts[::2],parts[1::2]))
        
        bme688 = OrderedDict((k, data_dict.get(k, None)) for k in bme688_keys)
        ips7100 = OrderedDict((k, data_dict.get(k,None)) for k in ips7100_keys)

        return{
            'timestamp': currentTime,
            'bme688':bme688,
            'ips7100':ips7100
        }
    except Exception as e:
        print("something went wrong in parse_data")
        return None
    
def write_to_csv(data):
    row = {'timestamp': data['timestamp']}
    row.update(data['bme688'])
    row.update(data['ips7100'])

    with open(csv_file, mode = 'a', newline = '') as f:
        writer = csv.DictWriter(f, fieldnames = all_keys)
        writer.writerow(row)

try:
    while True:
        raw_data = read_sensor()
        if raw_data:
            parsed = parse_data(raw_data)
            if parsed:
                write_to_csv(parsed)
                print('Saved to CSV:', parsed['timestamp'] )
        time.sleep(10)

except KeyboardInterrupt:
    print("'\nLogging stopped by user. Exiting cleanly.")
    ser.close()