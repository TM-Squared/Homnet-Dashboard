from django.contrib.auth.decorators import login_required
from django.urls import path

from .views import IndexView, addrouter, DetailRouter, ListRouters

app_name = "home"

urlpatterns = [
    path('', login_required(IndexView.as_view()), name="index"),
    path('addrouter', login_required(addrouter), name='addrouter'),
    path('listrouters', login_required(ListRouters.as_view()), name="listrouters"),
    path('detail/<uuid:serialnumber>', login_required(DetailRouter.as_view()), name='details')
]