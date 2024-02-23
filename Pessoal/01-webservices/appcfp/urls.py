from django.urls import path
from . import views


urlpatterns = [
    path('', views.Usuarios.login),
    path('login/', views.Usuarios.autenticacao, name='autenticacao'),
    path('home/', views.home, name='home'),
    path('logoff/', views.logoff, name='logoff'),
    path('clientes/', views.CadastroClientes._list, name='cliente-list'),
    path('clientesins/', views.CadastroClientes._insert, name='cliente-insert'),
    #path('clientesupd/', views.CadastroClientes.update, name='cliente-update'),
    #path('clientesdel/', views.CadastroClientes.delete, name='cliente-deletet'),
]