from django import forms
from django.forms import ModelForm, widgets

from app.models import Message


class GeoLookupForm(forms.Form):
    lat = forms.CharField()
    lng = forms.CharField()


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
                'class': "form-control",
                }),
            'subject': widgets.TextInput(attrs={
                'placeholder': 'Subject',
                'autofocus': True,
                'class': "form-control"
                }),
            'email': widgets.TextInput(attrs={
                'placeholder': 'Your email address',
                'class': "form-control"
                })
        }


