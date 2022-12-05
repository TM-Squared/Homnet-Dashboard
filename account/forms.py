from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import User


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "class": "login__input"
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "login__input"
            }
        )
    )


class RegisterForm(UserCreationForm):
    firstname = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder": "Enter First Name",
                "class": "form-control",
                "id":"exampleInputFirstName"
            }
        ))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "class": "login__input"
            }
        ))
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "class": "login__input"
            }
        ))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password check",
                "class": "login__input"
            }
        ))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
