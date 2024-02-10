from django.urls import path
from . import views


urlpatterns = [
    path('', views.login),
    path('', views.logoff, name='logoff'),
    path('login/', views.autenticacao, name='autenticacao'),
    path('home/', views.home, name='home'),
    path('tabelas/', views.tabelas_lista, name='tabelas-lista'),
    path('selects/', views.selects_lista, name='selects-lista'),
    path('configuracoes/', views.configuracoes, name='configuracoes'),
]