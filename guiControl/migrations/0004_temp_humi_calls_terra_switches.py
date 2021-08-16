# Generated by Django 3.2.5 on 2021-08-15 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guiControl', '0003_alter_light_interval_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Temp_humi_calls',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp', models.FloatField()),
                ('humidety', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Terra_switches',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lights_switch', models.CharField(max_length=100)),
                ('fans_switch', models.CharField(max_length=100)),
                ('misting_switch', models.CharField(max_length=100)),
            ],
        ),
    ]
