import ros_api
import uuid
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.views import generic

from .forms import RouterForm
from .models import Routers, Interface


# Create your views here.
class IndexView(generic.ListView):
    model = Routers
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['routers'] = Routers.objects.all()
        return context


def addrouter(request):
    context = {}
    if request.method == 'POST':
        serialnumber = str(uuid.uuid4())
        form = RouterForm(request.POST)
        context['form'] = form
        if form.is_valid():
            addrouter_data = request.POST.dict()
            username = addrouter_data.get("username")
            ipaddress = addrouter_data.get("ipaddress")
            password = addrouter_data.get("password")
            enterprise = addrouter_data.get("enterprise")
            print(username, ipaddress, password, enterprise)
            if check_if_interface_is_online(username=username, ipaddress=ipaddress, password=password):
                password_save = make_password(password)
                saverouter = Routers(serialnumber=generate_serial_number(), username=username,
                                     routername=get_router_name(username=username, ipaddress=ipaddress,
                                                                password=password), password=password_save,
                                     enterprise=enterprise)
                saverouter.save()
                for interface in list_interfaces_with_ip_address(username=username, ipaddress=ipaddress,
                                                                 password=password):
                    Interface(nom=interface['name'],
                              type=interface['type'],
                              ipaddress=interface['address'],
                              router=saverouter
                              ).save()

                return redirect('home:index')
            else:
                error_message = "we cannot connect to router via this interface"
                print(error_message)
                context['errors'] = error_message
                return render(request, "home/addrouter.html", context)
        else:
            print("form is not valid")
            return render(request, "home/addrouter.html", context)
    else:
        form = RouterForm()
        context['form'] = form
        return render(request, "home/addrouter.html", context)


class ListRouters(generic.ListView):
    model = Routers
    template_name = "home/listRouters.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['routers'] = Routers.objects.all()
        return context


class DetailRouter(generic.DetailView):
    template_name = 'home/detailRouter.html'
    model = Routers

    def get_object(self, queryset=None):
        return Routers.objects.get(serialnumber=self.kwargs.get("serialnumber"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['router_information'] = self.get_object()
        return context


def check_if_interface_is_online(username, ipaddress, password):
    router = ros_api.Api(ipaddress, user=username, password=password)
    return router.is_alive()


def list_interfaces_with_ip_address(username, ipaddress, password):
    router = ros_api.Api(ipaddress, user=username, password=password)
    interfaces = router.talk("/interface/print")
    addressips = router.talk("/ip/address/print")
    for addressip in addressips:
        for interface in interfaces:
            if addressip['interface'] == interface['name']:
                interface['address'] = addressip['address']

    return interfaces


def get_router_name(username, ipaddress, password):
    router = ros_api.Api(ipaddress, user=username, password=password)
    routername = router.talk("/system/identity/print")
    return routername[0]['name']


def generate_serial_number():
    return str(uuid.uuid4())
