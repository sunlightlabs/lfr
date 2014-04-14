from django import forms
from django.forms import ModelForm, widgets

from app.models import Message


class GeoLookupForm(forms.Form):
    lat = forms.CharField()
    lng = forms.CharField()


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'person_id', 'message', 'email']
        widgets = {
            'person_id': widgets.HiddenInput(),
            'message': widgets.Textarea(),
        }


class PasswordForm(forms.Form):
    password = forms.CharField()
    remember_me = forms.BooleanField()
    class Meta:
       widgets = {
            'password': forms.PasswordInput(attrs={
                'class': 'input-block-level',
                'placeholder': 'Password',
                }),
        }


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
    remember_me = forms.BooleanField()
    class Meta:
       widgets = {
            'password': forms.PasswordInput(attrs={
                'class': 'input-block-level',
                'placeholder': 'Password',
                }),
            'email': forms.EmailInput(attrs={
                'class': 'input-block-level',
                'placeholder': 'Email address',
                }),
        }


class ResetPasswordForm(forms.Form):
    email = forms.EmailField()
    class Meta:
       widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'input-block-level',
                }),
        }