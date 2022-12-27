from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):

    def create_user(self, email, firstname=None, lastname=None, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email, firstname, lastname, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        user = self.create_user(email=email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.save()

        return user
