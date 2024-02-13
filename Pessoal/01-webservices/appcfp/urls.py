from django.urls import path
from . import views


urlpatterns = [
    path('', views.login),
    path('login/', views.autenticacao, name='autenticacao'),
    path('home/', views.home, name='home'),
    path('', views.logoff, name='logoff'),
    path('clientes/', views.CadastroClientes.view, name='cliente-list'),
    path('clientesins/', views.CadastroClientes.insert, name='cliente-insert'),
    path('clientesupd/', views.CadastroClientes.update, name='cliente-update'),
    path('clientesdel/', views.CadastroClientes.delete, name='cliente-deletet'),
]