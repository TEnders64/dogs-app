# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core import serializers
from .models import *
# Create your views here.
def index(request):
    context = {
        # 'rates': Rate.objects.filter(date__range=(three_ago, today))
        'rates': Rate.objects.all().order_by('-date')

    }
    return render(request, "dogs/index.html", context)

def rate(request):
    print request.POST
    if 'old' in request.POST:
        # entering an older rate
        incoming_date = request.POST['date'].split('-') # '2019-01-14'
        incoming_time = request.POST['time'].split(':') # '15:45'
        year = incoming_date[0]
        month = incoming_date[1]
        day = incoming_date[2]
        hour = incoming_time[0]
        minute = incoming_time[1]
        Rate.objects.create(rate=request.POST['rate'], date=datetime(year, month, day, hour, minute))
    else:
        Rate.objects.create(rate=request.POST['rate'], date=datetime.now())
    return redirect("/")

def pastrates(request, num):
    today = datetime.now() 
    diff = today - timedelta(days=int(num))
    context = {
        'rates': Rate.objects.filter(date__range=(diff, today)).order_by('-date')
    }
    return render(request, "dogs/index.html", context)

def pastrates_json(request, num):
    today = datetime.now() 
    if int(num) is 0:
        data = Rate.objects.all().order_by('-date')
    else:
        diff = today - timedelta(days=int(num))
        data = Rate.objects.filter(date__range=(diff, today)).order_by('-date')
    outgoing_data = serializers.serialize("json", data) 
    return JsonResponse(outgoing_data, safe=False)