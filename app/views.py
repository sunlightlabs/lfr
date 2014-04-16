import urllib
import operator

import requests

from django.conf import settings
from django.core import urlresolvers, mail

from django.views.generic import edit
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache

from django.template import loader
from django.template.response import TemplateResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.shortcuts import render, redirect
from django.contrib import messages

from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import (
    user_passes_test, login_required, permission_required)
from django.contrib.contenttypes.models import ContentType

from . import forms
from .models import Message, LfrUser


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
        redirected to `confirm_message_sent` which is where all the
        auth(entication|orization) checking happens.
        '''
        return urlresolvers.reverse(
            'confirm_message_sent', args=(self.object.id,))

    def get_initial(self):
        '''Prepopulate the form the requested person_id and the user's
        email if she's logged in.
        '''
        initial_data = dict(self.request.GET.items())
        if self.request.user.is_authenticated():
            initial_data['email'] = self.request.user.email
        return initial_data

    def form_valid(self, form):
        '''If the user is not logged in, create a passwordless
        account for them and consider them logged in.
        '''
        # Create new user if necessary.
        if not self.request.user.is_authenticated():
            email = form.data['email']
            User = get_user_model()
            user, created = User.objects.get_or_create(email=email)
            if created:
                # Set a dummy password and log the new user in.
                user.set_password('doggy')
                user.save()
                user = authenticate(email=user.email, password='doggy')
                user.set_unusable_password()
                login(self.request, user)
            else:
                # Here the user exists but isn't logged in.
                # They'll get prompted for passwd at authorize_message.
                # Make a email address available to the login view.
                self.request.session['email'] = email

        # Trigger the form save.
        redirect_resp = super().form_valid(form)

        # Store the message for later confirmation view.
        self.request.session['message_id'] = self.object.id

        return redirect_resp


@login_required
@permission_required('app.add_message', login_url=settings.VERIFY_EMAIL_URL)
def confirm_message_sent(request, message_id):
    '''This ensures the user is authenticated, has been prompted for a
    password, and has a verified email address. After that, it sends
    the message request off to earwig.
    '''
    message = Message.objects.get(id=message_id)
    ctx = dict(message=message)
    return render(request, 'app/confirm_message_sent.html', ctx)


def email_verification_prompt(request):
    '''Send the email to start email verification.

    See django.contrib.auth.forms.PasswordResetForm
    '''
    ctx = {
        'email': request.user.email,
        'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
        'user': request.user,
        'domain': settings.LFR_DOMAIN,
        'token': default_token_generator.make_token(request.user),
        'protocol': 'https' if request.is_secure() else 'http',
    }
    email_template = 'app/email/verify_email/body'
    subject_template = 'app/email/verify_email/subject.txt'
    subject = loader.render_to_string(subject_template, ctx)
    subject = ''.join(subject.splitlines())
    body_txt = loader.render_to_string(email_template + '.txt', ctx)
    body_html = loader.render_to_string(email_template + '.html', ctx)
    from_email = settings.LFR_EMAIL_SENDER
    to = request.user.email

    msg = mail.EmailMultiAlternatives(subject, body_txt, from_email, [to])
    msg.attach_alternative(body_html, "text/html")
    msg.send()
    return render(request, 'app/verify_email_prompt.html', {})


@sensitive_post_parameters()
@never_cache
def email_verification_confirmation(request, uidb64=None, token=None,
       token_generator=default_token_generator,
       post_reset_redirect=None,
       current_app=None, extra_context=None):
    '''User visited the email verification link.

    See django.contrib.auth.view.password_reset_confirm
    '''
    UserModel = get_user_model()
    assert uidb64 is not None and token is not None  # checked by URLconf
    try:
        uid = urlsafe_base64_decode(uidb64)
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):

        # Mark the user as verified.
        user.is_verified = True
        user.save()

        # Log the user in.
        if not user.is_authenticated:
            login(request, user)

        # Grant message-save permission.
        content_type = ContentType.objects.get_for_model(Message)
        add_message = Permission.objects.get(codename='add_message')
        user.user_permissions.add(add_message.id)

        # XXX: Also send activation request to Earwig.
        pass

        return redirect('email_verification_complete')
    else:
        template_name='app/verify_email_invalid.html',
        return render(request, template_name, {})


def email_verification_complete(request):
    if not request.user.is_authenticated:
        return render(request, 'app/verify_email_complete.html', {})

    # Flash a confirmation message.
    messages.success(request, 'Your account was successfully activated.')

    # If no password set yet, suggest setting password.
    if request.user.has_unusable_password():
        tmpl = '''
            To make logging in easier next time, please
            <a href="{% url 'django.contrib.auth.views.password_reset' %}">
            set your password.</a>
            '''
        messages.warning(request, loader.render_to_string(tmpl))

    # Forward to the pending message.
    message_id = request.session.pop('message_id')
    return redirect(
        urlresolvers.reverse('confirm_message_sent', args=(message_id,)))