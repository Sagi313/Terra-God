from guiControl.models import Device, Humi_sensor, Led_screen, Light_interval, Temp_humi_calls, Terra_switches
from django.shortcuts import redirect, render
from django.contrib import messages


def index(response):    
    switches = Terra_switches.objects.first() # TODO: Change this. When first installing there is nothing in the DB, not even 1 row.
    
    sensor_records = Temp_humi_calls.objects.last() # TODO: change to the last 10 calls
    
    if response.method == 'POST':
        print(response.POST, flush=True)

        if response.POST.get('lights_switch'):
            switches.lights_switch = response.POST.get('lights_switch')
        elif response.POST.get('fans_switch'):
            switches.fans_switch = response.POST.get('fans_switch')
        elif response.POST.get('misting_switch'):
            switches.misting_switch = response.POST.get('misting_switch')
        
        switches.save()
        return redirect('/')

    return render(response, "guiControl/index.html", {'temp': sensor_records.temp, 'humi': sensor_records.humidity,
                                                      'switches': switches})


def lights(response):
    
    if response.method == 'POST':
        if response.POST.get("submit"):
            associated_device = Device.objects.get(name=response.POST.get('device'))
            
            new_inter = Light_interval(name=response.POST.get('interval_name'), status='running', device=associated_device, start_time=response.POST.get('start_time'), end_time=response.POST.get('end_time'))
            new_inter.save()

            messages.success(response, f'Interval {new_inter.name} added succuessfully')


        if response.POST.get("delete_intervals"):
            for key in response.POST:
                if "delete-inter_" in key:
                    to_delete_id = key.split("_")[1]
                    to_delete_inter = Light_interval.objects.get(id=int(to_delete_id))
                    inter_name = to_delete_inter.name
                    to_delete_inter.delete()

                    messages.success(response, f'Interval {inter_name} was deleted')

        return redirect('/lights')

    # Gets only the intervals that has a device in the correct type
    def get_all_relevant_intervals():
        relevant_intervals = []
        all_intervals = Light_interval.objects.all()

        for inter in all_intervals:
            related_device = Device.objects.get(id=inter.device.id)
            if related_device.type == "Light":
                relevant_intervals.append(inter)
        
        return relevant_intervals

    return render(response, "guiControl/intervals.html", {'intervals':get_all_relevant_intervals(), 'devices':Device.objects.all(), 'interval_type':"Light"})


def misting(response):

    if response.method == 'POST':
        if response.POST.get("submit"):
            associated_device = Device.objects.get(name=response.POST.get('device'))
            
            new_inter = Light_interval(name=response.POST.get('interval_name'), status='running', device=associated_device, start_time=response.POST.get('start_time'), end_time=response.POST.get('end_time'))
            new_inter.save()

            messages.success(response, f'Interval {new_inter.name} added succuessfully')


        if response.POST.get("delete_intervals"):
            for key in response.POST:
                if "delete-inter_" in key:
                    to_delete_id = key.split("_")[1]
                    to_delete_inter = Light_interval.objects.get(id=int(to_delete_id))
                    inter_name = to_delete_inter.name
                    to_delete_inter.delete()

                    messages.success(response, f'Interval {inter_name} was deleted')

        return redirect('/misting')

    # Gets only the intervals that has a device in the correct type
    def get_all_relevant_intervals():
        relevant_intervals = []
        all_intervals = Light_interval.objects.all()

        for inter in all_intervals:
            related_device = Device.objects.get(id=inter.device.id)
            if related_device.type == "Misting":
                relevant_intervals.append(inter)
        
        return relevant_intervals

    return render(response, "guiControl/intervals.html", {'intervals':get_all_relevant_intervals(), 'devices':Device.objects.all(), 'interval_type':"Misting"})




def fans(response):
    if response.method == 'POST':
        if response.POST.get("submit"):
            associated_device = Device.objects.get(name=response.POST.get('device'))
            
            new_inter = Light_interval(name=response.POST.get('interval_name'), status='running', device=associated_device, start_time=response.POST.get('start_time'), end_time=response.POST.get('end_time'))
            new_inter.save()

            messages.success(response, f'Interval {new_inter.name} added succuessfully')


        if response.POST.get("delete_intervals"):
            for key in response.POST:
                if "delete-inter_" in key:
                    to_delete_id = key.split("_")[1]
                    to_delete_inter = Light_interval.objects.get(id=int(to_delete_id))
                    inter_name = to_delete_inter.name
                    to_delete_inter.delete()

                    messages.success(response, f'Interval {inter_name} was deleted')

        return redirect('/fans')

    # Gets only the intervals that has a device in the correct type
    def get_all_relevant_intervals():
        relevant_intervals = []
        all_intervals = Light_interval.objects.all()

        for inter in all_intervals:
            related_device = Device.objects.get(id=inter.device.id)
            if related_device.type == "Fans":
                relevant_intervals.append(inter)
        
        return relevant_intervals

    return render(response, "guiControl/intervals.html", {'intervals':get_all_relevant_intervals(), 'devices':Device.objects.all(), 'interval_type':"Fans"})


def other_devices(response):
    if response.method == 'POST':
        if response.POST.get("submit"):
            associated_device = Device.objects.get(name=response.POST.get('device'))
            
            new_inter = Light_interval(name=response.POST.get('interval_name'), status='running', device=associated_device, start_time=response.POST.get('start_time'), end_time=response.POST.get('end_time'))
            new_inter.save()

            messages.success(response, f'Interval {new_inter.name} added succuessfully')


        if response.POST.get("delete_intervals"):
            for key in response.POST:
                if "delete-inter_" in key:
                    to_delete_id = key.split("_")[1]
                    to_delete_inter = Light_interval.objects.get(id=int(to_delete_id))
                    inter_name = to_delete_inter.name
                    to_delete_inter.delete()

                    messages.success(response, f'Interval {inter_name} was deleted')

        return redirect('/other_devices')

    # Gets only the intervals that has a device in the correct type
    def get_all_relevant_intervals():
        relevant_intervals = []
        all_intervals = Light_interval.objects.all()

        for inter in all_intervals:
            related_device = Device.objects.get(id=inter.device.id)
            if related_device.type == "Other":
                relevant_intervals.append(inter)
        
        return relevant_intervals

    return render(response, "guiControl/intervals.html", {'intervals':get_all_relevant_intervals(), 'devices':Device.objects.all(), 'interval_type':"Other"})


def daemon_logs(response):
    return render(response, "guiControl/daemon_logs.html", {})

def settings(response):

    sensor = Humi_sensor.objects.first()
    screen = Led_screen.objects.first()

    if response.method == 'POST':
        if response.POST.get("apply_screen"):
            screen.pin_number = response.POST.get('screen_pin_num')
            screen.start_time = response.POST.get('screen_start')
            screen.end_time = response.POST.get('screen_end')
            screen.save()
        
        if response.POST.get("apply_sensor"):
            sensor.pin_number = response.POST.get('sensor_pin_num')
            sensor.save()
    
        return redirect('/settings')
    
    return render(response, "guiControl/settings.html", {'sensor': sensor, 'screen': screen})

def devices(response):

    if response.method == 'POST':

        if response.POST.get("submit"):
            try:
                new_dev = Device(name=response.POST.get('device_name'), pin_number=response.POST.get('pin_number'), type=response.POST.get('type'))
                new_dev.save()
        
                messages.success(response, f'Device {new_dev.name} was added successfully')
            except:
                messages.error(response, f'Could not add {new_dev.name}. Name and GPIO pin must be unique')

            return redirect('/devices')

        if response.POST.get("delete_devices"):

            for key in response.POST:
                if "delete-device_" in key:

                    to_delete_id = key.split("_")[1]
                    to_delete_dev = Device.objects.get(id=int(to_delete_id))
                    dev_name = to_delete_dev.name
                    to_delete_dev.delete()

                    messages.success(response, f'Device {dev_name} was deleted')

                   

    
    return render(response, "guiControl/devices.html", {'devices':Device.objects.all()})