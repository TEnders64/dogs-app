from django.conf.urls import url
from . import views 

urlpatterns = [
    url(r'^$', views.index),
    url(r'^rate$', views.rate),
    url(r'^rates/past/(?P<num>[0-9]+)$', views.pastrates),
    url(r'^rates/past/(?P<num>[0-9]+)/json$', views.pastrates_json),
]
