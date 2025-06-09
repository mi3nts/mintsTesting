from datetime import datetime, timezone
from gps_nmea import GPS_NMEA
from time import sleep

gps = GPS_NMEA(baudrate=115200, timeout=1)

while True:

    raw_data = gps.sensor_sensor()
    if not raw_data:
        print('No data read from sensor')
        continue


    rawData = gps.read_sensor()
    parsedData = gps.parse_data(rawData)
    result = gps.identify_sentences(parsedData)

    gps.export_to_csv(result)
    gps.save_to_yaml(result)

    time.sleep(2)
    