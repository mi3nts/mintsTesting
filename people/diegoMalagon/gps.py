from datetime import datetime, timezone
from gps_nmea import GPS_NMEA
from time import sleep

gps = GPS_NMEA(baudrate=115200, timeout=1)

while True:

    raw_data = gps.read_sensor()
    if not raw_data:
        print('No data read from sensor')
        continue


    parsedData = gps.parse_data(raw_data)
    result = gps.identify_sentences(raw_data)

    gps.export_to_csv(result)
    gps.save_to_yaml(result)

    sleep(2)
    