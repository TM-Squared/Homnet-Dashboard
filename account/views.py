from django.conf import settings
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .forms import LoginForm, RegisterForm


# Create your views here.
def login_view(request):
    context = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        context['form'] = form
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(email=email, password=password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect(settings.LOGIN_REDIRECT_URL)
            else:
                context['message'] = "Invalid Credentials"
    else:
        form = LoginForm()
        context['form'] = form
    print(context)
    return render(request, "account/login.html", context)


def register_user(request):
    context = {}
    if request.method == "POST":
        form = RegisterForm(request.POST)
        context['form'] = form
        if form.is_valid():
            form.save()
            context['message'] = "User created successfully"
            return redirect("account:login")
        else:
            return render(request, 'account/register.html', context)
    else:
        form = RegisterForm()
        context['form'] = form
    return render(request, "account/register.html", context)
