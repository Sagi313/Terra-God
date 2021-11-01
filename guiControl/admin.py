from django.contrib import admin
from django.contrib.admin.decorators import register
from .models import Humi_sensor, Led_screen, Light_interval, Temp_humi_calls, Terra_switches, Device, Daemon_stats

admin.site.register([Light_interval, Humi_sensor, Temp_humi_calls, Led_screen, Terra_switches, Device, Daemon_stats])
# Register your models here.
