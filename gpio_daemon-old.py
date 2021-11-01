#!/usr/bin/python3

import os
from time import sleep
import django
from datetime import datetime
import I2C_LCD_driver   # An external py file in the same path
import Adafruit_DHT


os.environ['DJANGO_SETTINGS_MODULE'] = 'TerrariumWeb.settings'
django.setup()
from guiControl.models import Interval, Terra_switches, Temp_humi_calls

# Code starts here
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

class Daemon():
    def lights_handler(switches):
        ### Lights ###
        if switches.lights_switch == "timer":
            print("by timer")
            for interval in Interval.objects.all():
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
            for interval in Interval.objects.all():
                light_pin = interval.pin_number
                GPIO.setup(light_pin, GPIO.OUT)
                GPIO.output(light_pin, GPIO.HIGH)
        
        else: # Switch off
            print("by on switch")
            for interval in Interval.objects.all():
                light_pin = interval.pin_number
                GPIO.setup(light_pin, GPIO.OUT)
                GPIO.output(light_pin, GPIO.LOW)

    def fans_handler(switches):
        pass

    def misting_handler(switches):
        pass

    def read_sensor():
        humidity_r, temperature_r = Adafruit_DHT.read_retry(11, 4)
        sen_read = Temp_humi_calls(temp=float(temperature_r), humidity=float(humidity_r))
        print(sen_read.temp, " , ", sen_read.humidity)
        #sen_read.save() # A problem with the save!!!! ####################################

    def screen_output(mylcd,curr_temp, curr_humi):
        # TODO: implement a timer for the screen
        #mylcd.lcd_clear()   # Might be useless. should be removed
        
        try:
            sensor_records = Temp_humi_calls.objects.last()
            curr_temp = sensor_records.temp
            curr_humi = sensor_records.humidity
        except:
            pass

        curr_humi, curr_temp = Adafruit_DHT.read_retry(11, 4)
        mylcd.lcd_display_string(f"Temp- {curr_temp} \n Humidity- {curr_humi}", 1)
        mylcd.lcd_display_string(f"Humidity- {curr_humi}", 2)

    def start():
        pass

    def stop():
        pass

mylcd = I2C_LCD_driver.lcd()

### main ###
try:
    while True:

        sleep(1)
        now = datetime.now().time().replace(microsecond=0)

        switches = Terra_switches.objects.get(id=1)  # Only 1 object should exist
        
        lights_handler(switches)
        fans_handler(switches)
        misting_handler(switches)
        read_sensor()

        screen_output(mylcd,"30.1", "99%")   # TODO: implement a sensor read for this data, then save tp DB and display


except:
    print("Error in the code (MINE)")
    mylcd.lcd_clear()
    GPIO.cleanup()

finally:
    mylcd.lcd_clear()
    GPIO.cleanup()

def main():
    import argparse
    parser = argparse.ArgumentParser(description="TerraGod- a daemon that handles the GPIO usage")
    parser.add_argument('command', help='Command: start | stop | restart')

    args = parser.parse_args()

    

    if args.command.lower() == 'start':
        pass
    elif args.command.lower() == 'stop':
        pass
    elif args.command.lower() == 'restart':
        pass
    else:
        print(f"Unknown command {args.command.lower()}")