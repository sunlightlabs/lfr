from django.conf.urls import patterns, url

from app.views import *


urlpatterns = patterns('app.views',
    url(r'^$', GeoLookup.as_view(), name='geo_lookup'),
    url(r'^compose_message/$', ComposeMessage.as_view(), name='compose_message'),
    url(r'^authorize_message/$', authorize_message, name='authorize_message'),
)
