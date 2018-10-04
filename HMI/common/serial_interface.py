import serial
import os 
import json

config_file = open('config.json', 'r')
config = json.load(config_file)

CONN = serial.Serial(write_timeout=0)
CONN.port = config['port']
CONN.baudrate = config['baud']

CONN.open()
#poll the sensor for the camera trigger