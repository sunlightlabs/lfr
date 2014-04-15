from django.conf.urls import patterns, include, url

from app.views import *


urlpatterns = patterns('',
    url(r'^', include('app.urls')),
    url(r'^', include('django.contrib.auth.urls')),
)

