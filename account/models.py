from django.contrib.auth.models import AbstractBaseUser
from django.db import models
from django.utils import timezone

from .managers import AccountManager


class CustumUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    firsname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now())

    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstname', 'lastname']

    objects = AccountManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.firsname + self.lastname

    def get_short_name(self):
        return self.firsname.split()[0]