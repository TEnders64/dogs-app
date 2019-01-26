# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from .models import *
# Create your views here.
def index(request):
    today = datetime.now() 
    three_ago = today - timedelta(days=5)
    
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