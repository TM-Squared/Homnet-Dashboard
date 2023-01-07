import ros_api
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import generic

from .forms import RouterForm
from .models import Routers, Interface
from .functions_utils import encrypt, Mikrotik, generate_serial_number


# Create your views here.

# Displays general information about administrated routers
class IndexView(generic.ListView):
    model = Routers
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['routers'] = Routers.objects.all()
        return context


# Form to save information about a router
def addrouter(request):
    context = {}
    if request.method == 'POST':
        form = RouterForm(request.POST)
        context['form'] = form
        if form.is_valid():
            addrouter_data = request.POST.dict()
            username = addrouter_data.get("username")
            ipaddress = addrouter_data.get("ipaddress")
            password = addrouter_data.get("password")
            enterprise = addrouter_data.get("enterprise")
            # print(username, ipaddress, password, enterprise)
            instance_mikrotik = Mikrotik(ipaddress, username, password)
            if instance_mikrotik.is_online():
                # encrypt password
                password_save = encrypt(password)
                # save information about routers on database
                saverouter = Routers(serialnumber=generate_serial_number(), username=instance_mikrotik.user,
                                     routername=instance_mikrotik.get_router_name(), enterprise=enterprise,
                                     password=password_save)
                saverouter.save()
                for interface in instance_mikrotik.list_interface_with_ip_address():
                    # save information about differents interfaces of router
                    Interface(nom=interface['name'],
                              type=interface['type'],
                              ipaddress=interface['address'],
                              router=saverouter
                              ).save()

                return redirect('home:index')
            else:
                error_message = "we cannot connect to router via this interface"
                # print(error_message)
                context['errors'] = error_message
                return render(request, "home/addrouter.html", context)
        else:
            # print("form is not valid")
            return render(request, "home/addrouter.html", context)
    else:
        form = RouterForm()
        context['form'] = form
        return render(request, "home/addrouter.html", context)


# List administrated routers
class ListRouters(generic.ListView):
    model = Routers
    template_name = "home/listRouters.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['routers'] = Routers.objects.all()
        return context


# Give information about specific router
class DetailRouter(generic.DetailView):
    template_name = 'home/detailRouter.html'
    model = Routers

    def get_object(self, queryset=None):
        return Routers.objects.get(serialnumber=self.kwargs.get("serialnumber"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        Interface.objects.filter(router=self.get_object().serialnumber)
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
            else:
                interface['address'] = ""

    return interfaces


def get_router_name(username, ipaddress, password):
    router = ros_api.Api(ipaddress, user=username, password=password)
    routername = router.talk("/system/identity/print")
    return routername[0]['name']
