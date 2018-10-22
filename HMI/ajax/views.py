from django.shortcuts import render, reverse
from django.http import JsonResponse, HttpResponseRedirect
import random
import os
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.files.storage import FileSystemStorage

from common.serial_interface import CONN
from common.vars import  ImageProcessor, update_event, EVENTS, set_global_interest_points, ErrorDetector
HEADER = int.from_bytes(b'H', byteorder='big')
FOOTER = int.from_bytes(b'F', byteorder='big')

def get_status(request):
    CONN.write(b'H100000F')
    resp = CONN.read(4)
    status = {
        'machineStatus': 'AUTO' if resp[1] else 'Manual',
        'boardCount': 0,
        'errorsFound': 0
    }
    return JsonResponse(status)

def get_color_status(request):
    CONN.write(b'H200000F')
    resp = CONN.read(6)
    while not resp[1] == HEADER and resp[5] == FOOTER:
        red = int.from_bytes(resp[2], byteorder='little')
        green = int.from_bytes(resp[3], byteorder='little')
        blue = int.from_bytes(resp[4], byteorder='little')
        print(red)
        status = {
            'status': 'Auto' if resp[1] else 'Manual',
            'currentColor': {
                'red': red,
                'green': green,
                'blue': blue
            }
        }
        resp = CONN.read(6)
    return JsonResponse(status)

@csrf_exempt
def get_snapshot(request):
    myfile = request.FILES['snapshot']
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    update_event('snapshot {} uploaded'.format(filename))
    ed = ErrorDetector('media/' + filename)
    ed.run()
    print(ed.error)
    update_event('{} error detected'.format(ed.error))
    if ed.error:
        CONN.write(bytes([72, 39, ed.error, ed.error, 0, 0, 70]))
        resp = CONN.read(1)
    return JsonResponse({'status': 'ok'})

@csrf_exempt
def image_upload(request):
    print(request.FILES)
    myfile = request.FILES['image']
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    update_event('Sample image {} uploaded'.format(filename))
    img_p = ImageProcessor('media/' + filename)
    img_p.process()
    set_global_interest_points(img_p.interest_points)
    update_event('{} Interest points obtained'.format(len(img_p.interest_points)))

    return HttpResponseRedirect(reverse('dashboard:dashboard'))

def toggle_printer(request):
    CONN.write(b'H700000F')
    resp = CONN.read(1)
    print(resp)
    return JsonResponse({'status': 'ok'})

def toggle_machine_mode(request):
    update_event('Machine mode toggled')
    CONN.write(b'H300000F')
    resp = CONN.read(1)
    print(resp)
    return JsonResponse({'status': 'ok'})

def toggle_color_mode(request):
    update_event('Color mode toggled')
    CONN.write(b'H400000F')
    resp = CONN.read(1)
    print(resp)
    return JsonResponse({'status': 'ok'})

@csrf_exempt
def set_color_setpoint(request):
    #message of three bytes 
    #rgb must be less than 256
    # message code 8 corresponds to int 56
    color_data = json.loads(request.body)
    msg = [HEADER, 
            56, 
            int(color_data['red']), 
            int(color_data['green']), 
            int(color_data['blue']), 
            0,
            0, 
            FOOTER]
    CONN.write(bytes(msg))
    resp = CONN.read(1)
    print(resp)
    return JsonResponse({'status': 'ok'})

def toggle_pigment_valve(request):
    CONN.write(b'H500000F')
    resp = CONN.read(1)
    print(resp)
    return JsonResponse({'status': 'ok'})

def toggle_base_valve(request):
    CONN.write(b'H600000F')
    resp = CONN.read(1)
    print(resp)
    return JsonResponse({'status': 'ok'})

def toggle_agitator(request):
    CONN.write(b'H000000F')
    resp = CONN.read(1)
    print(resp)
    return JsonResponse({'status': 'ok'})

@csrf_exempt
def get_register_positions(request):
    data = json.loads(request.body)
     
    CONN.write(bytes([72,
       39, 
       int(data['unitOne']),
       int(data['unitTwo']),
       0, 
       0, 
       70]))
    resp = CONN.read(1)
    
    return JsonResponse({'status': 'ok'})

def get_events(request):
    global EVENTS
    return JsonResponse({'events': EVENTS})