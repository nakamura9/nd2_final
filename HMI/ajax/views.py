from django.shortcuts import render
from django.http import JsonResponse
import random
from django.views.decorators.csrf import csrf_exempt

from common.serial_interface import CONN
from common import harris


def get_status(request):
    CONN.write(b'H100000F')
    resp = CONN.read(4)
    print(resp)
    status = {
        'machineStatus': 'AUTO' if resp[1] else 'Manual',
        'boardCount': resp[2],
        'errorsFound': random.randint(1, 100)
    }
    return JsonResponse(status)

def get_color_status(request):
    CONN.write(b'H200000F')
    resp = CONN.read(6)
    print(resp)
    status = {
        'status': 'Auto' if resp[1] else 'Manual',
        'currentColor': str(resp[2]) + str(resp[3]) + 
            str(resp[4])
    }
    return JsonResponse(status)

@csrf_exempt
def image_upload(request):
    return JsonResponse({'status': 'ok'})

def toggle_printer(request):
    CONN.write(b'H700000F')
    resp = CONN.read(1)
    print(resp)
    return JsonResponse({'status': 'ok'})

def toggle_machine_mode(request):
    CONN.write(b'H300000F')
    resp = CONN.read(1)
    print(resp)
    return JsonResponse({'status': 'ok'})


def toggle_color_mode(request):
    CONN.write(b'H400000F')
    resp = CONN.read(1)
    print(resp)
    return JsonResponse({'status': 'ok'})


def set_color_setpoint(request):
    CONN.write(b'H8' + bytes(request.GET['color']) +  b'00F')
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

def get_register_positions(request):
    #testing with 4 
    CONN.write(b'H944000F')
    resp = CONN.read(1)
    print(resp)
    return JsonResponse({'status': 'ok'})

#will these be necessary?
def get_interest_points(request):
    #get image file
    #run harris detection on it
    #use calibration data to measure lengths 
    #return list of interest points
    
    return JsonResponse({'interest_points': []})

def get_events(request):
    return JsonResponse({'events': []})