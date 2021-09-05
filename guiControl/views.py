from guiControl.models import Humi_sensor, Led_screen, Light_interval, Temp_humi_calls, Terra_switches
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import os


def index(response):    
    switches = Terra_switches.objects.get(id=1)
    
    sensor_records = Temp_humi_calls.objects.last() # TODO: change to the last 10 calls
    
    if response.method == 'POST':
        if "lights_switch_timer" in  response.POST:
            switches.lights_switch = "timer"

        if "lights_switch_on" in  response.POST:
            switches.lights_switch = "on"

        if "lights_switch_off" in  response.POST:
            switches.lights_switch = "off"
        
        switches.save()
        return HttpResponseRedirect('/')



    return render(response, "guiControl/index.html", {'temp':sensor_records.temp , 'humi': sensor_records.humidity})

def lights(response):
    interval1 = [{'name':'Jungle Dawn', 'status':'running', 'pin_number':'7', 'start_time':'10:00', 'end_time': '15:45'}]
    
    if response.method == 'POST':
        if response.POST.get("submit"):
            # Will be replaced with DB objects
            newInst = {'name': response.POST.get('interval_name'), 'status': 'running', 'pin_number': response.POST.get('pin_number'), 'start_time':response.POST.get('start_time'), 'end_time':response.POST.get('end_time') }
            interval1.append(newInst)

            new_inter = Light_interval(name=newInst['name'], status=newInst['status'], pin_number= newInst['pin_number'], start_time= newInst['start_time'], end_time= newInst['end_time'])
            new_inter.save()



        if response.POST.get("delete_intervals"):
            for key in response.POST:
                if "delete-inter_" in key:
                    to_delete_name = key.split("_")[1]
                    to_delete_inter = Light_interval.objects.get(id=int(to_delete_name))
                    to_delete_inter.delete()

        return HttpResponseRedirect('/lights')

        

    return render(response, "guiControl/lights.html", {'intervals': Light_interval.objects.all()})


def misting(response):
    return render(response, "guiControl/misting.html", {})


def fans(response):
    return render(response, "guiControl/fans.html", {})

def settings(response):

    sensor = Humi_sensor.objects.get(id=1)
    screen = Led_screen.objects.get(id=1)

    if response.method == 'POST':
        if response.POST.get("apply_screen"):
            screen.pin_number = response.POST.get('screen_pin_num')
            screen.start_time = response.POST.get('screen_start')
            screen.end_time = response.POST.get('screen_end')
            screen.save()
        
        if response.POST.get("apply_sensor"):
            sensor.pin_number = response.POST.get('sensor_pin_num')
            sensor.save()
    
        return HttpResponseRedirect('/settings')
    
    return render(response, "guiControl/settings.html", {'sensor': sensor, 'screen': screen})