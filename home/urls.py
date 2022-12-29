from django.urls import path

from .views import index, addrouter, listrouters, detailsRouter

app_name = "home"

urlpatterns = [
    path('', index, name="index"),
    path('addrouter', addrouter, name='addrouter'),
    path('listrouters', listrouters, name="listrouters"),
    path('detailsrouter', detailsRouter, name='detailsrouter')
]