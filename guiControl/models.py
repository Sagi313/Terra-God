from django.db import models

class Light_interval(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    pin_number = models.IntegerField(default=0)
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
    temp = models.FloatField()
    humidety = models.FloatField()

    def __str__(self):
        return (f"temp- {self.temp}, humidety- {self.humidety}")