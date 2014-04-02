from django import forms


class GeoLookupForm(forms.Form):
    lat = forms.CharField()
    lng = forms.CharField()