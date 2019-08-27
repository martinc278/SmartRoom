from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from .settings import *
import requests


# App models
from .models import Chair, Measure


# Create your views here.
# index: main view
def index(request):
    if request.method == 'POST' and 'connect_sensors' in request.POST:
        return connect_sensors()

    list_measures = Measure.objects.order_by('-date').distinct()[0:MEASURES_DISPLAYED]
    context = {'list_measures': list_measures, }
    print(request)
    return render(request, 'ConnectedChairs/index.html', context)


def connect_sensors():
    # get all IP
    ip_list = []
    list_chairs = get_list_or_404(Chair)
    for chair in list_chairs:
        ip_list.append(chair.ip)

    print(ip_list)  # comment in production

    data = {}  # {'ip':{'distance': 1, 'temperature':2}, {...}}

    # processing : connect to sensors and get values
    for ip in ip_list:
        try:
            url = 'http://'+ip+'/json'
            resp = requests.get(url=url)
        except requests.exceptions.RequestException as ex:
    	    # print(ex)
    	    data[ip] = {'temperature':'N/A', 'distance':'N/A'}
       	else:
       		chair_data = resp.json()
       		data[ip] = {'temperature': str(chair_data['Sensors'][0]['TaskValues'][0]['Value']) + ' D. Celsius',
                     'distance': str(chair_data['Sensors'][1]['TaskValues'][0]['Value']) + ' cm'}
       		
    
    # Update databse with new measures data
    for ip, sensors in data.items():
    	my_chair = get_object_or_404(Chair, ip=ip)
    	meas = Measure()
    	meas.idc = my_chair
    	meas.sensor_distance = sensors['distance']
    	meas.sensor_temperature = sensors['temperature']
    	meas.date = timezone.now()
    	meas.save()

    # Update databse with new measures data
    # for ip in ip_list:
    #    my_chair = get_object_or_404(Chair, ip=ip)
    #    meas = Measure()
    #    meas.idc = my_chair
    #    meas.sensor_distance = '10'
    #    meas.sensor_temperature = '10'
    #    meas.date = timezone.now()
    #    meas.save()

    # Remove data more than MEASURES_PERSISTENCE long
    list_measures = get_list_or_404(Measure)
    for meas in list_measures:
        if meas.was_measured_recently() is False:
            Measure.objects.filter(pk=meas.pk).delete()

    return HttpResponseRedirect(reverse('index'))


# detail: chair view
def detail(request, chair_id):
    chair = get_object_or_404(Chair, idc=chair_id)
    list_measures = get_list_or_404(Measure.objects
                                    .order_by('-date'),
                                    idc=chair_id)
    context = {'chair': chair,
               'list_measures': list_measures,
               }
    return render(request, 'ConnectedChairs/detail.html', context)
