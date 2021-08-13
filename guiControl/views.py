from guiControl.models import Light_interval
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import os


def index(response):
    return render(response, "guiControl/index.html", {})

def lights(response):
    interval1 = [{'name':'Jungle Dawn', 'status':'running', 'pin_number':'7', 'start_time':'10:00', 'end_time': '15:45'}]
    
    if response.method == 'POST':
        if response.POST.get("submit"):
            # Will be replaced with DB objects
            newInst = {'name': response.POST.get('interval_name'), 'status': 'running', 'pin_number': response.POST.get('pin_number'), 'start_time':response.POST.get('start_time'), 'end_time':response.POST.get('end_time') }
            interval1.append(newInst)

            new_inter = Light_interval(name=newInst['name'], status=newInst['status'], pin_number= newInst['pin_number'], start_time= newInst['start_time'], end_time= newInst['end_time'])
            new_inter.save()



        if response.POST.get("delete_intervals"):
            for key in response.POST:
                if "delete-inter_" in key:
                    to_delete_name = key.split("_")[1]
                    print(f"Hereee- {to_delete_name}", flush=True)
                    to_delete_inter = Light_interval.objects.get(id=int(to_delete_name))
                    to_delete_inter.delete()

        return HttpResponseRedirect('/lights')

        

    return render(response, "guiControl/lights.html", {'intervals': Light_interval.objects.all()})


def misting(response):
    return render(response, "guiControl/misting.html", {})


def fans(response):
    return render(response, "guiControl/fans.html", {})