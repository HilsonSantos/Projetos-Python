from django.urls import path
from .views import (
    home,
    grupos_lista,
    grupo_novo,
    grupo_editar,
    grupo_excluir,
    usuarios_lista,
    usuario_novo,
    usuario_editar,
    usuario_excluir,
    login_view, cadastro_paciente, logout_view,
)

urlpatterns = [
    path("", home, name="home"),
    path("login/", login_view, name="login"),
    path("cadastro/", cadastro_paciente, name="cadastro_paciente"),
    path("sair/", logout_view, name="logout"),
    path("usuarios/", usuarios_lista, name="usuarios_lista"),
    path("usuarios/novo/", usuario_novo, name="usuario_novo"),
    path("usuarios/<int:pk>/editar/", usuario_editar, name="usuario_editar"),
    path("usuarios/<int:pk>/excluir/", usuario_excluir, name="usuario_excluir"),
    path("grupos/", grupos_lista, name="grupos_lista"),
    path("grupos/novo/", grupo_novo, name="grupo_novo"),
    path("grupos/<int:pk>/editar/", grupo_editar, name="grupo_editar"),
    path("grupos/<int:pk>/excluir/", grupo_excluir, name="grupo_excluir"),
]
