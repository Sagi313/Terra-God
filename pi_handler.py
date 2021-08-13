import os
from time import sleep
import django
from datetime import datetime

os.environ['DJANGO_SETTINGS_MODULE'] = 'TerrariumWeb.settings'
django.setup()
from guiControl.models import Light_interval

# Code starts here
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

while True:
    sleep(0.5)
    now = datetime.now().time().replace(microsecond=0)
    for interval in Light_interval.objects.all():
        light_pin = interval.pin_number
        GPIO.setup(light_pin, GPIO.OUT)

        if interval.start_time <= now and now <= interval.end_time:
            GPIO.output(light_pin, GPIO.HIGH)
            print(f"{interval.start_time} < {now} < {interval.end_time}")

        else:
            GPIO.output(light_pin, GPIO.LOW)
            print(f"{interval.start_time} not {now} not {interval.end_time}")