import datetime

import ros_api

from django.contrib import messages
from django.views import generic
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from .forms import RouterForm
from .models import Routers, Logs
from .functions_utils import encrypt, generate_serial_number, check_if_router_is_online, decrypt


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
        # context['logs'] = Logs.objects.all()
        return context

    def get_queryset(self):
        """:return: all logs"""
        return Logs.objects.all()


# Form to save information about a router
class AddRouter(FormView):
    template_name = "home/addrouter.html"
    form_class = RouterForm
    success_url = reverse_lazy('home:index')

    def form_valid(self, form):
        addrouter_data = self.request.POST
        username = addrouter_data["username"]
        ipaddress = addrouter_data["ipaddress"]
        password = addrouter_data["password"]
        enterprise = addrouter_data["enterprise"]

        connexion_mikrotik = ros_api.Api(ipaddress, user=username, password=password)
        if connexion_mikrotik.is_alive():
            password_save = encrypt(password)
            saverouter = Routers(serialnumber=generate_serial_number(), username=username,
                                 routername=connexion_mikrotik.talk("/system/identity/print")[0]['name'],
                                 enterprise=enterprise,
                                 ipaddress=ipaddress,
                                 password=password_save)
            saverouter.save()
            messages.success(self.request, "Saved Router")
            for log in connexion_mikrotik.talk("/log/print"):
                Logs(time=datetime.datetime.combine(datetime.date.today(),
                                                    datetime.time(*map(int, log['time'].split(":")))),
                     topics=log['topics'].replace(",", "."),
                     message=log['message'],
                     router=saverouter).save()

            return super().form_valid(form)
        else:
            messages.error(self.request, "We can't connect to Router")
            return super().form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


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
        # context['routers'] = Routers.objects.all()
        return context


# Give information about specific router
class DetailRouter(generic.DetailView):
    template_name = 'home/detailRouter.html'
    model = Routers

    def get_object(self, queryset=None):
        return Routers.objects.get(serialnumber=self.kwargs.get("serialnumber"))

    def setup(self, request, **kwargs):
        super().setup(request, **kwargs)
        router = self.get_object()
        self.connexion = ros_api.Api(user=router.username, password=decrypt(router.password),
                                     address=router.ipaddress)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['interfaces'] = [{k.replace("-", "_"): v for k, v in information.items()}
                                 for information in self.connexion.talk("/interface/print")]
        context['ports'] = [{k.replace("-", "_"): v for k, v in information.items()}
                            for information in self.connexion.talk("/port/print")]
        context['operating_statistics'] = [{k.replace("-", "_"): v for k, v in information.items()}
                                           for information in self.connexion.talk("/system/resource/print")]
        context['active_users'] = [{k.replace("-", "_"): v for k, v in information.items()}
                                   for information in self.connexion.talk("/user/active/print")]
        context['ipaddresses'] = [{k.replace("-", "_"): v for k, v in information.items()}
                                  for information in self.connexion.talk("/ip/address/print")]
        context['ports'] = [{k.replace("-", "_"): v for k, v in information.items()}
                            for information in self.connexion.talk("/port/print")]
        context['files'] = [{k.replace("-", "_"): v for k, v in information.items()}
                            for information in self.connexion.talk("/file/print")]
        context['packages'] = [{k.replace("-", "_"): v for k, v in information.items()}
                               for information in self.connexion.talk("/system/package/print")]
        context['daily_data_streams'] = [
            {'name': interface['name'], 'rx_byte': interface['rx-byte'], 'tx_byte': interface['tx-byte'],
             'rx_packet': interface["rx-packet"], 'tx_packet': interface["tx-packet"]}
            for interface in self.connexion.talk("/interface/print")]

        print(context["daily_data_streams"])

        return context
