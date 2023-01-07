from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .managers import AccountManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    firstname = models.CharField(max_length=255, blank=True)
    lastname = models.CharField(max_length=255, blank=True)
    data_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'

    objects = AccountManager()

    def __str__(self):
        return self.email

    '''
    :return the firstname + lastname with a space between
    '''

    def get_full_name(self):
        return self.firsname + self.lastname

    '''
    :return firstname for the user
    '''

    def get_short_name(self):
        return self.firsname

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
