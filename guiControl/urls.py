from django.urls import path

from . import views

app_name = 'Terrarium Pi'
urlpatterns = [
    path('', views.index, name='index'),
    path('lights/', views.lights, name='Lights'),
    path('fans/', views.fans, name='fans'),
    path('misting/', views.misting, name='misting'),
    path('devices/', views.devices, name='devices'),
    path('daemon_logs/', views.daemon_logs, name='daemon logs'),
    path('other_devices/', views.other_devices, name='other devices'),
    path('sensors/', views.sensors, name='sensors'),
    path('settings/', views.settings, name='settings'),
]

