from django.urls import path

from . import views

app_name = 'Terrarium Pi'
urlpatterns = [
    path('', views.index, name='index'),
    path('lights/', views.lights, name='Lights'),
    path('fans/', views.fans, name='fans'),
    path('misting/', views.misting, name='misting'),
    path('settings/', views.settings, name='settings'),
]

