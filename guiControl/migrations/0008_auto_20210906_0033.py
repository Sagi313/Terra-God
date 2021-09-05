# Generated by Django 3.2.5 on 2021-09-05 21:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guiControl', '0007_alter_temp_humi_calls_read_rime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='temp_humi_calls',
            name='read_rime',
        ),
        migrations.AddField(
            model_name='temp_humi_calls',
            name='read_time',
            field=models.TimeField(default=datetime.datetime(2021, 9, 6, 0, 33, 22, 810623)),
        ),
    ]