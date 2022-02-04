from django.contrib import admin
from .models import Humi_sensor, Led_screen, Light_interval, Temp_humi_calls, Terra_switches, Device, Daemon_stats, \
    IntervalGroup

admin.site.register(
    [Light_interval, Humi_sensor, Temp_humi_calls, Led_screen, Terra_switches, Device, Daemon_stats, IntervalGroup])
# Register your models here.
