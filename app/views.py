import urllib
import operator

import requests

from django.conf import settings
from django.core import urlresolvers
from django.views.generic import edit
# from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
# from django.contrib import messages

from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required, permission_required
# from django.views.decorators.http import require_POST

from . import forms
from .models import Message


class GeoLookup(edit.FormView):
    template_name = 'app/geo_lookup.html'
    form_class = forms.GeoLookupForm

    def form_valid(self, form):
        url = 'http://api.opencivicdata.org/people/'
        params = dict(
            name=form.data['address'],
            apikey=settings.SUNLIGHT_API_KEY)
        resp = requests.get(url, params=params)
        people = resp.json()['results']
        ctx = dict(people=people)
        return render(self.request, 'app/results.html', ctx)


class ComposeMessage(edit.CreateView):
    model = Message
    form_class = forms.MessageForm

    @property
    def success_url(self):
        '''When users successfully submit the form, they get
        redirected to `authorize_messages` which is where all the
        auth(entication|orization) checking happens.
        '''
        return urlresolvers.reverse('authorize_message')

    def get_initial(self):
        '''Prepopulate the form the requested person_id and the user's
        email if she's logged in.
        '''
        initial_data = dict(self.request.GET.items())
        if self.request.user.is_authenticated():
            initial_data['email'] = user.email
        return initial_data

    def form_valid(self, form):
        '''If the user is not logged in, create a passwordless
        account for them and consider them logged in.
        '''
        if not self.request.user.is_authenticated():
            email = form.data['email']
            User = get_user_model()
            user, created = User.objects.get_or_create(email=email)
            if created:
                # Set a dummy password and log the new user in.
                user.set_unusable_password()
                login(self.request, user)
            else:
                # Here the user exists but isn't logged in.
                # They'll get prompted for passwd at authorize_message.
                pass
        return super().form_valid(form)


def prompt_for_password(user):
    return user.has_unusable_password()


class EnterPassword(edit.FormView):
    template_name = 'login.html'
    template_name = 'enter_password.html'
    form_class = forms.PasswordForm

    def get_context_data(self, **kwargs):
        kwargs['prompt'] = 'Please enter your password'
        return kwargs

    def form_valid(self, form):
        import pdb; pdb.set_trace()


class Login(edit.FormView):
    template_name = 'login.html'
    form_class = forms.LoginForm

    def get_context_data(self, **kwargs):
        kwargs.update(
            prompt='Please sign in',
            show_reset=True)
        return kwargs

    def form_valid(self, form):
        import pdb; pdb.set_trace()


class ResetPassword(edit.FormView):
    template_name = 'reset_password.html'
    form_class = forms.ResetPasswordForm

    def form_valid(self, form):
        '''Generate password reset token and send password reset email.
        '''
        import pdb; pdb.set_trace()


@login_required
@user_passes_test(prompt_for_password, login_url=settings.SET_PASSWORD_URL)
@permission_required('app.add_message', login_url=settings.VERIFY_EMAIL_URL)
def authorize_message(request):
    '''This ensures the user is authenticated, has been prompted for a
    password, and has a verified email address. After that, it sends
    the message request off to earwig.
    '''
    import pdb; pdb.set_trace()


