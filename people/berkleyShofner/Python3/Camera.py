import cv2
import csv
import os
import time
import datetime
import numpy as np
from collections import OrderedDict

time = datetime.datetime.now()

video = cv2.VideoCapture(4)

check, frame = video.read()

blue = np.sum(frame[:, :, 0])
green = np.sum(frame[:, :, 1])
red = np.sum(frame[:, :, 2])

cameraDictionary = OrderedDict([
    ("dateTime", time),
    ("Blue", blue),
    ("Green", green),
    ("Red", red),
    ])

keys =  list(cameraDictionary.keys())
exists = os.path.isfile("/home/berkley/Documents/Python3/Camera.csv")
with open('Camera.csv', 'a') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=keys)
    if(not(exists)):
        writer.writeheader()
    writer.writerow(cameraDictionary)

cv2.imshow("Capturing", frame)

cv2.waitKey(5)

video.release()
