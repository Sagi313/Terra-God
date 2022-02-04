#!/usr/bin/env python
 
import django
import Adafruit_DHT
import I2C_LCD_driver   # An external py file in the same path
import RPi.GPIO as GPIO
from datetime import datetime
import sys, time, os, logging
from base_daemon import Daemon



os.environ['DJANGO_SETTINGS_MODULE'] = 'TerrariumWeb.settings'
django.setup()
from guiControl.models import Device, Terra_switches, Temp_humi_calls, Light_interval

 
class MyDaemon(Daemon):
    def __init__(self,pidfile):
        logging.basicConfig(filename='/var/log/gpio-daemon.log', filemode='w', level=logging.DEBUG)
        super().__init__(pidfile)
        GPIO.setmode(GPIO.BOARD)
        self.mylcd = I2C_LCD_driver.lcd()


    def run(self):
        while True:
            time.sleep(1)
            
            logging.debug(f'Runnning {datetime.now().time()}')

            self.interval_handler()
            self.read_sensor()
            self.screen_output(self.mylcd,"30.1", "99%")   # TODO: implement a sensor read for this data, then save tp DB and display

    ### THIS IS THE NEW APPROCH TO IMPLEMENT. THIS SHOULD BE REPLACED WITH THE CURRENT FUNCTION ###

    def merge_time_intervals(self, pin_to_interval_map):  # TODO: Fix that to be by each pin, not a type.
        merged = []
        for pin_number, interval_list in pin_to_interval_map.items():
            merged = [interval_list.pop(0)]
            for interval in interval_list:
                if merged[-1].end_time < interval.start_time:
                    merged.append(interval)
                elif merged[-1].end_time > interval.start_time and interval.end_time > merged[-1].end_time:
                    merged[-1].end_time = interval.end_time

        return merged

    def change_switches(self, switch_state, merged_intervals):
        if switch_state == 'timer':
            for interval in merged_intervals:
                now = datetime.now().time()

                pin_number = interval.device.pin_number
                GPIO.setup(pin_number, GPIO.OUT)

                if interval.start_time < now and now < interval.end_time:
                    GPIO.output(pin_number, GPIO.LOW)

                else:
                    GPIO.output(pin_number, GPIO.HIGH)

        elif switch_state == 'on':
            for interval in merged_intervals:
                light_pin = interval.device.pin_number
                GPIO.setup(light_pin, GPIO.OUT)
                GPIO.output(light_pin, GPIO.LOW)

        else:   # Off switch
            for interval in merged_intervals:
                light_pin = interval.device.pin_number
                GPIO.setup(light_pin, GPIO.OUT)
                GPIO.output(light_pin, GPIO.HIGH)

    def interval_handler(self):
        switches = Terra_switches.objects.first()
        logging.info(f'All the switches statuses: {switches}')

        all_intervals =  Light_interval.objects.all()

        lights_intervals, fans_intervals, misting_intervals = [], [], []
        for interval in all_intervals:
            if interval.device.type == 'Light':
                lights_intervals.append(interval)
            elif interval.device.type == 'Fans':
                fans_intervals.append(interval)
            elif interval.device.type == 'Misting':
                misting_intervals.append(interval)

        lights_pin_num_to_interval_map = {}
        for interval in lights_intervals:
            if str(interval.device.pin_number) in lights_pin_num_to_interval_map:
                lights_pin_num_to_interval_map[str(interval.device.pin_number)] += [interval]
            else:
                lights_pin_num_to_interval_map[str(interval.device.pin_number)] = [interval]

        fans_pin_num_to_interval_map = {}
        for interval in fans_intervals:
            if str(interval.device.pin_number) in fans_pin_num_to_interval_map:
                fans_pin_num_to_interval_map[str(interval.device.pin_number)] += [interval]
            else:
                fans_pin_num_to_interval_map[str(interval.device.pin_number)] = [interval]

        misting_pin_num_to_interval_map = {}
        for interval in misting_intervals:
            if str(interval.device.pin_number) in misting_pin_num_to_interval_map:
                misting_pin_num_to_interval_map[str(interval.device.pin_number)] += [interval]
            else:
                misting_pin_num_to_interval_map[str(interval.device.pin_number)] = [interval]

        print(lights_pin_num_to_interval_map)
        lights_merged_intervals = self.merge_time_intervals(lights_pin_num_to_interval_map)
        fans_merged_intervals = self.merge_time_intervals(fans_pin_num_to_interval_map)
        misting_merged_intervals = self.merge_time_intervals(misting_pin_num_to_interval_map)
        print(lights_merged_intervals)

        self.change_switches(switches.lights_switch, lights_merged_intervals)
        self.change_switches(switches.fans_switch, fans_merged_intervals)
        self.change_switches(switches.misting_switch, misting_merged_intervals)
        



    # def interval_handler(self):
    #     logging.info('Started checking intervals')
    #     switches = Terra_switches.objects.first()
    #     logging.info(f'All the switches statuses: {switches}')

    #     for interval in Light_interval.objects.all():
    #         related_device = Device.objects.get(id=interval.device)

    #         device_group = related_device.type
    #         device_group_status = ''
    #         if device_group == 'Light':
    #             device_group_status = switches.lights_switch 
    #         elif device_group == 'Fans':
    #             device_group_status = switches.fans_switch 
    #         elif device_group == 'Misting':
    #             device_group_status = switches.misting_switch 
            
    #         logging.info(f'device {interval} status: {device_group_status}')

    #         if device_group_status == "timer":
    #             logging.info(f'{interval} is by timer')
    #             now = datetime.now().time()

    #             light_pin = interval.device.pin_number
    #             GPIO.setup(light_pin, GPIO.OUT)

    #             if interval.start_time < now and now < interval.end_time:
    #                 GPIO.output(light_pin, GPIO.LOW)
    #                 print(f"{interval.start_time} < {now} < {interval.end_time}")

    #             else:
    #                 GPIO.output(light_pin, GPIO.HIGH)
    #                 print(f"{interval.start_time} not {now} not {interval.end_time}")
            

    #         elif device_group_status == "off" and related_device.status == 'Running':    # Always off. Ignores the timer
    #             logging.info(f'{interval} is by off switch')
    #             light_pin = interval.device.pin_number

    #             GPIO.setup(light_pin, GPIO.OUT)
    #             GPIO.output(light_pin, GPIO.HIGH)
            
            
    #         elif device_group_status == "on" and related_device.status == 'Stopped':    # Always on. Ignores the timer
    #             logging.info(f'{interval} is by on switch')
    #             light_pin = interval.device.pin_number
    #             GPIO.setup(light_pin, GPIO.OUT)
    #             GPIO.output(light_pin, GPIO.LOW)

    #     logging.info('Checked all the intervals')

    def read_sensor(self):
        humidity_r, temperature_r = Adafruit_DHT.read_retry(11, 4)
        sen_read = Temp_humi_calls(temp=float(temperature_r), humidity=float(humidity_r))
        logging.info(f'temp-{sen_read.temp} ; humidity-{sen_read.humidity}')
        #sen_read.save() # A problem with the save!!!! ####################################

    def screen_output(self, mylcd, curr_temp, curr_humi):
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


if __name__ == "__main__":
    daemon = MyDaemon('/tmp/gpio-daemon.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        print("usage: %s start|stop|restart" % sys.argv[0])
        sys.exit(2)