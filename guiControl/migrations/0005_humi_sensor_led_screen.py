# Generated by Django 3.2.5 on 2021-08-15 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guiControl', '0004_temp_humi_calls_terra_switches'),
    ]

    operations = [
        migrations.CreateModel(
            name='Humi_sensor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pin_number', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Led_screen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pin_number', models.IntegerField(default=0)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
        ),
    ]