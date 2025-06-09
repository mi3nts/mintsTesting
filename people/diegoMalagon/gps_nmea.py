import serial
from collections import OrderedDict
import csv
import os
from datetime import datetime
import yaml

class GPS_NMEA:
    def __init__(self, baudrate = 115200, timeout = 1, port='/dev/tty.usbmodem1101'):
        self.baudrate = baudrate
        self.timeout = timeout
        self.port = port

    #TODO: make this read lines dynamically, not just grab 5 lines
    def read_sensor(self):        
        try:
            with serial.Serial(port = self.port, baudrate=self.baudrate, timeout=self.timeout) as ser:
                sentence_list = []
                for i in range(5):
                    line = ser.readline().decode('utf-8').strip()
                    sentence_list.append(line)
                print("RAW SENSOR DATA: ", sentence_list)
                return sentence_list
        except serial.SerialException as e:
            print(f"SERIAL ERROR: {e}")
            return None

    def parse_data(self, raw_data):
        sentences = []
        for data in raw_data:
            fields = data.split(",")
            sentences.append(fields)
        return sentences
            

    def identify_sentences(self, sentences):
        result = {k: None for k in ['$GPRMC', '$GPVTG', '$GPGGA', '$GPGSA', '$GPGLL']}
        
        for sentence in sentences:
            parts = sentence.split(',')

            try:
                match parts[0]:
                    case '$GPRMC':
                            
                        time = ':'.join([parts[1][i:i+2] for i in range(0, len(parts[1]), 2)]) 

                        warning = parts[2]

                        # latitude calculations and string conversions
                        latitudeUnprocessed = float(parts[3])
                        latitudeDegrees = str(int(latitudeUnprocessed / 100)) + "B0"
                        latitudeMinutes = str(round(latitudeUnprocessed % 100, 2)) + "'"
                        latitude = str(latitudeDegrees) + str(latitudeMinutes) + parts[4]

                        # longitude calculations and string conversions
                        longitudeUnprocessed = float(parts[5])
                        longitudeDegrees = str(int(longitudeUnprocessed / 100)) + "B0"
                        longitudeMinutes = str(round(longitudeUnprocessed % 100, 2)) + "'"
                        longitude = str(longitudeDegrees)+ str(longitudeMinutes) + parts[6]

                        speedKnots = parts[7]
                        trueCourse = parts[8]
                        date = '/'.join([parts[9][i:i+2] for i in range(0, len(parts[9]), 2)]) 
                        magneticVariation = parts[10] + "B0"
                        magneticVariationDirection = parts[11].split('*')[0]       # ignore the checksum after the first character

                        result['$GPRMC'] = OrderedDict([
                            ('validity', f'{warning}'),
                            ('datetime', f"{date} {time}"),
                            ('coordinates', f'{latitude}, {longitude}'),
                            ('speed in knots', f'{speedKnots} knots'),
                            ('true course', f'{trueCourse}'),
                            ('magnetic variation', f'{magneticVariation} {magneticVariationDirection}')
                    ])
                    case "$GPVTG":
                        result['$GPVTG'] = OrderedDict([
                            ('true track', f'{parts[1]}B0 T'),
                            ('magnetic track', f'{parts[3]}B0 M'),
                            ('speed in knots', f'{parts[5]} knots'),
                            ('speed in km/h', f'{parts[7]} km/h')
                        ])
                    case "$GPGGA":

                        time = ':'.join([parts[1][i:i+2] for i in range(0, len(parts[1]), 2)])
                        
                        latitudeUnprocessed = float(parts[2])
                        latitudeDegrees = str(int(latitudeUnprocessed / 100)) + "B0"
                        latitudeMinutes = str(round(latitudeUnprocessed % 100, 2)) + "'"
                        latitude = str(latitudeDegrees) + str(latitudeMinutes) + parts[3]

                        longitudeUnprocessed = float(parts[4])
                        longitudeDegrees = str(int(longitudeUnprocessed / 100)) + "B0"
                        longitudeMinutes = str(round(longitudeUnprocessed % 100, 2)) + "'"
                        longitude = str(longitudeDegrees)+ str(longitudeMinutes) + parts[5]

                        fix_quality = parts[6]
                        satellites = parts[7]
                        hdop = parts[8]
                        altitude = f"{parts[9]} {parts[10]}"
                        geoidal_sep = f"{parts[11]} {parts[12]}"

                        result['$GPGGA'] = OrderedDict([
                        ('time (UTC)', time),
                        ('coordinates', f"{latitude}, {longitude}"),
                        ('fix quality', fix_quality),
                        ('satellites used', satellites),
                        ('HDOP', hdop),
                        ('altitude', altitude),
                        ('geoidal separation', geoidal_sep)
                        ])

                    case "$GPGSA":

                        mode = parts[1]
                        fix_type = parts[2]
                        satellites_used = [sv for sv in parts[3:15] if sv]
                        pdop = parts[15]
                        hdop = parts[16]
                        vdop = parts[17].split('*')[0]

                        result['$GPGSA'] = OrderedDict([
                        ('mode', 'Automatic' if mode == 'A' else 'Manual'),
                        ('fix type', {'1': 'No Fix', '2': '2D Fix', '3': '3D Fix'}.get(fix_type, 'Unknown')),
                        ('satellites used', ', '.join(satellites_used)),
                        ('PDOP', pdop),
                        ('HDOP', hdop),
                        ('VDOP', vdop)
                        ])

                    case "$GPGLL":

                        latitudeUnprocessed = float(parts[1])
                        latitudeDegrees = str(int(latitudeUnprocessed / 100)) + "B0"
                        latitudeMinutes = str(round(latitudeUnprocessed % 100, 2)) + "'"
                        latitude = str(latitudeDegrees) + str(latitudeMinutes) + parts[2]

                        longitudeUnprocessed = float(parts[3])
                        longitudeDegrees = str(int(longitudeUnprocessed / 100)) + "B0"
                        longitudeMinutes = str(round(longitudeUnprocessed % 100, 2)) + "'"
                        longitude = str(longitudeDegrees)+ str(longitudeMinutes) + parts[4]

                        time = ':'.join([parts[5][i:i+2] for i in range(0, len(parts[5]), 2)])
                        status = 'Valid' if parts[6] == 'A' else 'Invalid'

                        result['$GPGLL'] = OrderedDict([
                            ('time_UTC', time),
                            ('latitude', latitude),
                            ('longitude', longitude),
                            ('status', status)

                        ])

            except Exception as e:
                print(f'Error parsing {parts[0]}: {e}')
        return result

    def export_to_csv(self, result, filename = 'gps_data.csv'):
        
        single_row = self.flatten_result(result)
        single_row['timestamp'] = datetime.utcnow().isoformat()

        file_exists = False
        try:
            with open(filename, 'r', newline = '') as f:
                file_exists = True
        except FileNotFoundError:
            print('file not found...')
            pass

        with open(filename, 'a', newline = '') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = single_row.keys())

            if not file_exists:
                writer.writeheader()

                writer.writerow(single_row)
                print(f'appended to {filename}: {single_row}')

    def save_to_yaml(self, result, filename = 'gps_log.yaml'):
        timestamp = datetime.utcnow().isoformat()
        flat_result = self.flatten_result(result)
        flat_result['timestamp'] = timestamp

        with open(filename, 'a') as file:
            yaml.dump(flat_result, file, sort_keys = False)
            file.write('\n---\n')

    def flatten_result(self, result):
        flattened = {}
        for sentence_type, data in result.items():
            if data is not None:
                for key, value in data.items():
                    flat_key = f"{sentence_type[1:]}_{key}" # remove $ and name sentence_type key
                    flattened[flat_key] = value # attach a value to new key
        return flattened