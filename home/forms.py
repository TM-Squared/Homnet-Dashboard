from django import forms
from .models import Routers


class RouterForm(forms.Form):
    username = forms.CharField(
        label='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    ipaddress = forms.GenericIPAddressField(
        label="IP Address",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        ))
    enterprise = forms.CharField(
        label="Enterprise",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
