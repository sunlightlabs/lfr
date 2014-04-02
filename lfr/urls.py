from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'lfr.views.home', name='home'),
    url(r'^results/$', 'lfr.views.results', name='results'),
    url(r'^admin/', include(admin.site.urls)),
)
