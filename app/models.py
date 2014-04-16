import json
import logging
import requests
from urllib.parse import urljoin

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.utils import timezone

from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin)


class EarwigMessageError(Exception):
    '''Raised if earwig push fails.
    '''


class Message(models.Model):
    '''Represents a submitted message.
    '''
    subject = models.CharField(max_length=255)
    person_id = models.CharField(max_length=255)
    person_name = models.CharField(max_length=255)
    message = models.TextField()
    email = models.EmailField()
    created = models.DateTimeField(default=timezone.now)

    @property
    def user(self):
        return get_user_model().objects.get(email=self.email)

    def __str__(self):
        tmpl = 'from %r to %r'
        return tmpl % (self.email, self.person_name)

    def send_to_earwig(sender, instance, **kwargs):
        '''Send this message to earwig, then delete the local
        copy.
        '''
        # If in debug mode, send messages to self.
        if settings.DEBUG:
            person_id = settings.EARWIG_DEBUG_PERSON_ID
        else:
            person_id = instance.person_id
        user = instance.user
        data = dict(
            type='email',
            subject=instance.subject,
            message=instance.message,
            sender=json.dumps(dict(
                email=instance.email,
                name=instance.person_name,
                ttl=settings.EARWIG_TTL)),
            recipients=person_id,
            user_email_verified=user.is_verified,
            key=settings.EARWIG_KEY)
        url = urljoin(settings.EARWIG_URL, 'message/')
        if settings.DEBUG:
            msg = 'Sending earwig message: %r'
            logging.getLogger().warning(msg % data)
        resp = requests.post(url, data=data)
        if not resp.status_code == 200:
            msg = 'Got status %d from earwig' % resp.status_code
            raise EarwigMessageError(msg)


post_save.connect(Message.send_to_earwig, sender=Message)


class LfrUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class LfrUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = LfrUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email
