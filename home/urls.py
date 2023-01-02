from django.urls import path

from .views import IndexView, addrouter, DetailRouter, ListRouters

app_name = "home"

urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('addrouter', addrouter, name='addrouter'),
    path('listrouters', ListRouters.as_view(), name="listrouters"),
    path('detail/<uuid:serialnumber>', DetailRouter.as_view(), name='detailsrouter')
]