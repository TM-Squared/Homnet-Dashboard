from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from .managers import AccountManager


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    firsname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = AccountManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.firsname + self.lastname

    def get_short_name(self):
        return self.firsname.split()[0]

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
