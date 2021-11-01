#!/usr/bin/env python3

import os
from time import sleep
import django
from datetime import datetime


os.environ['DJANGO_SETTINGS_MODULE'] = 'TerrariumWeb.settings'
django.setup()
from guiControl.models import Terra_switches, Temp_humi_calls, Light_interval

# Code starts here
humidity_r, temperature_r = 17 , 25
sen_read = Temp_humi_calls(temp=float(temperature_r), humidity=float(humidity_r))
print(sen_read.temp, " , ", sen_read.humidity)
sen_read.save() # A problem with the save!!!! ####################################
# Code starts here

inter = Light_interval.objects.get(id=6)
print(inter.device.pin_number)