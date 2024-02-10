from django.urls import path
from . import views


urlpatterns = [
    path('', views.login),
    path('login/', views.autenticacao, name='autenticacao'),
    path('home/', views.home, name='home'),
    path('', views.logoff, name='logoff'),
    path('clientes/', views.clientes_listar, name='clientes-listar'),
]