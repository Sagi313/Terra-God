#!/usr/bin/env python3

import os
from time import sleep
import django
from datetime import datetime
import I2C_LCD_driver   # An external py file in the same path

os.environ['DJANGO_SETTINGS_MODULE'] = 'TerrariumWeb.settings'
django.setup()
from guiControl.models import Light_interval, Terra_switches

# Code starts here
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

def lights_handler(switches):
    ### Lights ###
    if switches.lights_switch == "timer":
        print("by timer")
        for interval in Light_interval.objects.all():
            light_pin = interval.pin_number
            GPIO.setup(light_pin, GPIO.OUT)

            if interval.start_time <= now and now <= interval.end_time:
                GPIO.output(light_pin, GPIO.LOW)
                print(f"{interval.start_time} < {now} < {interval.end_time}")

            else:
                GPIO.output(light_pin, GPIO.HIGH)
                print(f"{interval.start_time} not {now} not {interval.end_time}")
    
    elif switches.lights_switch == "off":    # Always off. Ignores the timer
        print("by off switch")
        for interval in Light_interval.objects.all():
            light_pin = interval.pin_number
            GPIO.setup(light_pin, GPIO.OUT)
            GPIO.output(light_pin, GPIO.HIGH)
    
    else: # Switch off
        print("by on switch")
        for interval in Light_interval.objects.all():
            light_pin = interval.pin_number
            GPIO.setup(light_pin, GPIO.OUT)
            GPIO.output(light_pin, GPIO.LOW)

def fans_handler(switches):
    pass

def misting_handler(switches):
    pass

def read_sensor():
    pass

def screen_output(mylcd,curr_temp, curr_humi):
    # TODO: implement a timer for the screen
    mylcd.lcd_clear()   # Might be useless. should be removed
    
    mylcd.lcd_display_string(f"Temp- {curr_temp} \n Humidity- {curr_humi}", 1)
    mylcd.lcd_display_string(f"Humidity- {curr_humi}", 2)

mylcd = I2C_LCD_driver.lcd()

try:
    while True:

        sleep(0.5)
        now = datetime.now().time().replace(microsecond=0)

        switches = Terra_switches.objects.get(id=1)  # Only 1 object should exist
        
        lights_handler(switches)
        fans_handler(switches)
        misting_handler(switches)

        screen_output(mylcd,"30.1", "100%")   # TODO: implement a sensor read for this data, then save tp DB and display


except:
    GPIO.cleanup()

finally:
    GPIO.cleanup()



