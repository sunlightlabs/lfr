import urllib

import requests

from django.conf import settings
from django.views.generic.edit import FormView
# from django.http import HttpResponse, Http404
# from django.shortcuts import render, redirect
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.http import require_POST


from .forms import GeoLookupForm


class Home(FormView):
    template_name = 'geo_lookup.html'
    form_class = GeoLookupForm
    success_url = '/results/'

    def post(self, request):
        url = 'http://api.opencivicdata.org/divisions'
        params = dict(
            lat=request.POST['lat'],
            lon=request.POST['lng'],
            apikey=settings.SUNLIGHT_API_KEY)
        resp = requests.get(url, params=params)

        url = 'http://api.opencivicdata.org/organizations'
        params = dict(
            division_id={'$in': },
            apikey=settings.SUNLIGHT_API_KEY)
        resp = requests.get(url, params=params)

        import pdb; pdb.set_trace()


home = Home.as_view()


def results(request):
    import pdb; pdb.set_trace()