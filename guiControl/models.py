from datetime import datetime
from django.db import models


class Device(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    pin_number = models.IntegerField(default=0, unique=True)
    type = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default="Dummy")
    is_disabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Light_interval(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return self.name   

class Terra_switches(models.Model):
    lights_switch = models.CharField(max_length=100)
    fans_switch = models.CharField(max_length=100)
    misting_switch = models.CharField(max_length=100)

    def __str__(self):
        return (f"Lights- {self.lights_switch}, Fans- {self.fans_switch}, Misting- {self.misting_switch}")

class Temp_humi_calls(models.Model):
    temp = models.FloatField(default=0.0)
    humidity = models.FloatField(default=0.0)
    read_time = models.TimeField(default=datetime.now)

    def __str__(self):
        return (f"temp- {self.temp}, humidity- {self.humidity}")

class Humi_sensor(models.Model):
    pin_number = models.IntegerField(default=0)

    def __str__(self):
        return (f"Humi pin- {self.pin_number}")

class Led_screen(models.Model):
    pin_number = models.IntegerField(default=0)
    start_time = models.TimeField()
    end_time = models.TimeField()


class Daemon_stats(models.Model):
    updated_at = models.TimeField()

