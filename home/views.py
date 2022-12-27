from django.shortcuts import render, redirect


# Create your views here.

def index(request):
    return render(request, "home/index.html")


def addrouter(request):
    return render(request, "home/addrouter.html")


def listrouters(request):
    return render(request, "home/listRouters.html")


def detailsRouter(request):
    return render(request, "home/detailRouter.html")