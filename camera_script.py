from gpiozero import Button
import requests
import os
from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (640, 320)
camera.start_preview()
# Camera warm-up time
sleep(2)

img_path = os.path.join(os.getcwd(), 'captured', 'img.jpeg')
RUNNING = True

btn = Button(2)
def upload_img():
    global img_path
    url = 'http://localhost:8000/api/get-snapshot'
    files = {'snapshot': open('img.jpeg', 'rb')}
    requests.post(url, files=files)

while RUNNING:
    btn.wait_for_press()
    btn.wait_for_release()
    camera.capture('img.jpeg')
    upload_img()
