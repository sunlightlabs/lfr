from django.conf.urls import patterns, include, url

from app.views import *


urlpatterns = patterns('',
    url(r'^', include('app.urls')),
    url(r'^', include('django.contrib.auth.urls')),
    url(r'^password_set/$', 'app.views.password_set', name='password_set'),
)

