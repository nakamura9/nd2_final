from django.shortcuts import render, reverse
from django.http import JsonResponse, HttpResponseRedirect
import random
import os
from django.views.decorators.csrf import csrf_exempt

from django.core.files.storage import FileSystemStorage

from common.serial_interface import CONN
from common.vars import  ImageProcessor, update_event, EVENTS, set_global_interest_points, ErrorDetector


def get_status(request):
    CONN.write(b'H100000F')
    resp = CONN.read(4)
    status = {
        'machineStatus': 'AUTO' if resp[1] else 'Manual',
        'boardCount': resp[2],
        'errorsFound': random.randint(1, 100)
    }
    return JsonResponse(status)

def get_color_status(request):
    CONN.write(b'H200000F')
    resp = CONN.read(6)
    print(resp[2:5])
    status = {
        'status': 'Auto' if resp[1] else 'Manual',
        'currentColor': str(resp[2]) + str(resp[3]) + 
            str(resp[4])
    }
    return JsonResponse(status)

@csrf_exempt
def get_snapshot(request):
    print(request.FILES)
    myfile = request.FILES['snapshot']
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    update_event('snapshot {} uploaded'.format(filename))
    ed = ErrorDetector('media/' + filename)
    ed.run()
    print(ed.error)
    update_event('{} error detected'.format(ed.error))
    if ed.error:
        CONN.write(bytes([b'H', b'9', ed.error, ed.error, 0, 0, b'F']))
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
    return JsonResponse({'status': 'ok'})

def get_events(request):
    global EVENTS
    return JsonResponse({'events': EVENTS})