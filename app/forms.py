from django import forms
from django.forms import ModelForm, widgets

from app.models import Message


class GeoLookupForm(forms.Form):
    lat = forms.CharField(widget=widgets.HiddenInput(attrs={}))
    lng = forms.CharField(widget=widgets.HiddenInput(attrs={}))
    address = forms.CharField(widget=widgets.TextInput(attrs={
        'placeholder': 'e.g. 1818 N Street NW Washington, DC 20036',
        'class': "form-control input-lg transparent search",
        'size': '50'}))


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = [
            'subject', 'person_id', 'person_name',
            'message', 'email']
        widgets = {
            'person_id': widgets.HiddenInput(attrs={}),
            'person_name': widgets.HiddenInput(attrs={}),
            'message': widgets.Textarea(attrs={
                'placeholder': 'Type your message here.',
                'class': "form-control input-lg",
                }),
            'subject': widgets.TextInput(attrs={
                'placeholder': 'Subject',
                'autofocus': True,
                'class': "form-control input-lg"
                }),
            'email': widgets.TextInput(attrs={
                'placeholder': 'Your email address',
                'class': "form-control input-lg"
                })
        }


