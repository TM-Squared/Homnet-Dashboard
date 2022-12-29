from django import forms
from .models import Routers


class RouterForm(forms.ModelForm):

    class Meta:
        model = Routers
        fields = '__all__'
        widgets = {
            'Password': forms.PasswordInput()
        }
