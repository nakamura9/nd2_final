import serial
import os 
import json

config_file = open('config.json', 'r')
config = json.load(config_file)

CONN = serial.Serial(write_timeout=0)
CONN.port = '/dev/ttyUSB0'
'''config['port']'''
CONN.baudrate = config['baud']
#CONN.open()

