from collections import OrderedDict
from datetime import datetime, timezone
import time
import os
import sys
import glob

def add_temps_to_od(file_pattern):
    currentTime = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    zoneTemps = {}

    if sys.platform.startswith('linux'):
        try:
            file_paths = glob.glob(file_pattern)
            for path in file_paths:
                zone = os.path.basename(path)
                with open(os.path.join(path, 'temp')) as sensor:
                    sensorTemp = int(sensor.read().strip()) / 1000
                    zoneTemps[zone] = sensorTemp

        except FileNotFoundError:
            print(f"Error: Directory ({file_pattern}) does not exist")
        except NotADirectoryError:
            print(f"Error: {file_pattern} is not a directory")
        except PermissionError:
            print(f"Error: Permission denied to access {file_pattern}")
        except Exception as e:
            print(f"An exception occurred: {e}")
    else:
        print("Incorrect operating system; please use a Linux-based OS")

    od[currentTime] = zoneTemps

file_pattern = '/sys/class/thermal/thermal_zone*'
od = OrderedDict()

while True:
    print("Reading temperature from sensors...")
    add_temps_to_od(file_pattern)
    print(od)
    time.sleep(10)