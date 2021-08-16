import os
from time import sleep
import django
from datetime import datetime

os.environ['DJANGO_SETTINGS_MODULE'] = 'TerrariumWeb.settings'
django.setup()
from guiControl.models import Light_interval, Terra_switches

# Code starts here


while True:
    sleep(0.5)
    now = datetime.now().time().replace(microsecond=0)

    switches = Terra_switches.objects.get(id=1)  # Only 1 object should exist

    ### Lights ###
    if switches.lights_switch == "timer":
        for interval in Light_interval.objects.all():
            light_pin = interval.pin_number

            if interval.start_time <= now and now <= interval.end_time:
                print("Timer-On")

            else:
                print("Timer-Off")

    
    elif switches.lights_switch == "on":    # Always on. Ignores the timer
        for interval in Light_interval.objects.all():
            light_pin = interval.pin_number
            print("On")
    
    else: # Switch off
        for interval in Light_interval.objects.all():
            light_pin = interval.pin_number
            print("Off")
