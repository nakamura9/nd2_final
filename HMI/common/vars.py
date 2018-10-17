from common.harris import *
from PIL import Image
import numpy as np
import datetime
import math
import json

EVENTS = []
BOARD_COUNT = 0
ERROR_COUNT = 0
INTEREST_POINTS = []

def set_global_interest_points(points):
    global INTEREST_POINTS
    INTEREST_POINTS = points 

def increment_board_count():
    global BOARD_COUNT
    BOARD_COUNT += 1

def increment_error_count():
    global ERROR_COUNT 
    ERROR_COUNT += 1

def update_event(evt):
    global EVENTS
    time = datetime.datetime.now().time()
    EVENTS.append("{} ->{}".format(time, evt))

class ImageProcessor(object):
    def __init__(self, img):
        self.img = img
        self.interest_points = []

    def process(self):
        self.img_convert()
        coords = get_harris_points(compute_harris_response(self.img_array), 10)
        print(coords)
        self.get_interest_points(coords)

    def img_convert(self):
        self.img_array = np.array(Image.open(self.img).convert('L'))

    def get_interest_points(self, coords):
        
        for xy in coords:
            ip = InterestPoint(xy)
            ip.get_descriptor(self.img_array)
            self.interest_points.append(ip)
        

class InterestPoint(object):
    def __init__(self, coords):
        self.x = coords[0]
        self.y = coords[1]
        self.descriptor = None

    def get_descriptor(self, img, wid=5):
        self.descriptor = img[self.x - wid: self.x + wid + 1, 
                self.y - wid: self.y + wid + 1].flatten()


class ErrorDetector(object):

    def __init__(self, new_img):
        global INTEREST_POINTS
        self.reference_points = INTEREST_POINTS
        self.img = new_img
        self.load_calibration_data()

    def run(self):
        self.process_new_img()
        self.error = self.find_errors()

    def load_calibration_data(self):
        self.calibration_data = json.load(open('calibration.json', 'r'))
    
    def process_new_img(self):
        img_p = ImageProcessor(self.img)
        img_p.process()
        self.new_points = img_p.interest_points

    def find_errors(self):

        desc_ref = [ip.descriptor for ip in self.reference_points]
        desc_target = [ip.descriptor for ip in self.new_points]
        matches = match_twosided(desc_ref, desc_target)
        'for each match find the average distance in the y coordinate between them in pixels',
        'use scale factor to compare'
        distance = 0
        for match in matches:
            pos_1 = self.reference_points[match].y
            pos_2 = self.new_points[match].y
            distance += pos_1 - pos_2

        avg_distance = int(distance / len(matches))
        if avg_distance > self.calibration_data['errorToleranceMM']:
            increment_error_count()
            return self.convert_pixels_to_degrees(avg_distance)
        
        return 0
    
    def convert_pixels_to_degrees(self, dist):
        mm_per_pixel = self.calibration_data['viewLength'] / self.calibration_data['resolution']
        mm = dist * mm_per_pixel
        #s = r0 0 = s/r
        angle_in_rad = mm / (self.calibration_data['rollerDiameter'] / 2)
        return (angle_in_rad / (2 * math.pi)) * 360       

        

    
