from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from .forms import LoginForm, RegisterForm


# Create your views here.

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                msg = "Invalid Credentials"
        else:
            msg = "Error validating the form"
    return render(request, "account/login.html", {"form": form, "msg": msg})


def register_user(request):
    msg = None
    success = False

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            msg = "User created"
            success = True
            return redirect("account:login")
        else:
            msg = 'Form is not valid'
    else:
        form = RegisterForm()
    return render(request, "account/register.html", {"form": form, "msg":msg, "success":success})
