import datetime

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import generic

from .forms import RouterForm
from .models import Routers, Logs
from .functions_utils import encrypt, Mikrotik, generate_serial_number, check_if_router_is_online, decrypt


# Create your views here.

# Displays general information about administrated routers
class IndexView(generic.TemplateView):
    template_name = "home/index.html"
    context_object_name = "logs"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        routers = []
        for router in Routers.objects.all():
            router = vars(router)
            router.pop('password')
            router.pop('_state')
            if check_if_router_is_online(ipaddress=router['ipaddress']):
                router['status'] = True
                routers.append(router)
            else:
                router['status'] = False
                routers.append(router)
        context['routers'] = routers
        context['logs'] = Logs.objects.all()
        #context['logs'] = Logs.objects.all()
        return context

    def get_queryset(self):
        """:return: all logs"""
        return Logs.objects.all()


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
            # create instance Mikrotik
            instance_mikrotik = Mikrotik(ipaddress, username, password)
            if instance_mikrotik.is_online():
                # encrypt password
                password_save = encrypt(password)
                # save information about routers on database
                saverouter = Routers(serialnumber=generate_serial_number(), username=instance_mikrotik.user,
                                     routername=instance_mikrotik.get_router_name(), enterprise=enterprise,
                                     ipaddress=ipaddress,
                                     password=password_save)
                saverouter.save()
                messages.info(request, "Saved Router", fail_silently=True)
                for log in instance_mikrotik.get_logs():
                    Logs(time=datetime.datetime.combine(datetime.date.today(), datetime.time(*map(int,log['time'].split(":")))),
                         topics=log['topics'].replace(",","."),
                         message=log['message'],
                         router=saverouter).save()

                return redirect('home:index')
            else:
                # if we can't initialize connection with interface
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
        routers = []
        for router in Routers.objects.all():
            router = vars(router)
            router.pop('password')
            router.pop('_state')
            if check_if_router_is_online(ipaddress=router['ipaddress']):
                router['status'] = True
                routers.append(router)
            else:
                router['status'] = False
                routers.append(router)
        context['routers'] = routers
        #context['routers'] = Routers.objects.all()
        return context


# Give information about specific router
class DetailRouter(generic.DetailView):
    template_name = 'home/detailRouter.html'
    model = Routers

    def get_object(self, queryset=None):
        return Routers.objects.get(serialnumber=self.kwargs.get("serialnumber"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #print(self.get_object().ipaddress)
        #context['status'] = check_if_router_is_online(ipaddress=self.get_object().ipaddress)
        router = self.get_object()
        connexion = Mikrotik(user=router.username, password=decrypt(router.password), ipaddress=router.ipaddress)
        context['interfaces'] = connexion.get_interfaces()
        context['ports'] = connexion.get_available_port()
        context['operating_statistics'] = connexion.get_router_operating_statistic()
        context['active_users'] = connexion.get_active_users()
        context['ipaddresses'] = connexion.get_ip_address()
        context['router_information'] = router
        return context

"""
    def get_context_object_name(self, obj):
        router = self.get_object()
        connexion = Mikrotik(user=router.username, password=decrypt(router.password), ipaddress=router.ipaddress)
        context = {'interfaces': connexion.get_interfaces(), 'port': connexion.get_available_port(),
                   'operating_statistics': connexion.get_router_operating_statistic(),
                   'ipaddress': connexion.get_ip_address()}
        return context

"""
