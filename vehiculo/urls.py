from django.urls import path
from . import views
from .views import vehiculo_add_view, register_view, login_view, logout_view, vehiculos_view

urlpatterns = [
    path('', views.index, name='index'),
    path('vehiculo/add/', vehiculo_add_view, name='vehiculoadd'),
    path('vehiculo/list/', vehiculos_view, name='vehiculoslist'),
    path('registro/', register_view, name='registro'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
