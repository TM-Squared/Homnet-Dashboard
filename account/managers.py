from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):

    def create_user(self, firstname, lastname, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email, firstname, lastname, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def superuser(self, email, firstname, lastname, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, firstname, lastname, password, **extra_fields)