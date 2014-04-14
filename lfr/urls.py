from django.conf.urls import patterns, include, url

from app.views import *


urlpatterns = patterns('',
    url(r'^', include('app.urls')),
    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^enter_password/$', EnterPassword.as_view(), name='enter_password'),
    url(r'^reset_password/$', ResetPassword.as_view(), name='reset_password'),
)
