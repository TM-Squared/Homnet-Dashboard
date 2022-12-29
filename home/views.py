from django.shortcuts import render, redirect
import ros_api

from .forms import RouterForm
from .models import Routers


# Create your views here.

def index(request):
    return render(request, "home/index.html")


def addrouter(request):
    if request.method == 'POST':
        form = RouterForm(request.POST)
        if form.is_valid():
            router = form.save()
            return render(request, 'home/listRouters.html')
        else:
            return render(request, "home/addrouter.html", {'form': form})
    else:
        form = RouterForm()
        return render(request, "home/addrouter.html", {'form': form})


def listrouters(request):
    router = Routers.objects.all()
    return render(request, "home/listRouters.html", )


def detailsRouter(request):
    return render(request, "home/detailRouter.html")


def check_if_interface_is_online(username, ipaddress, password):
    router = ros_api.Api(ipaddress, user=username, password=password)
    return router.is_alive()
