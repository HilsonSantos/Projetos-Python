from django.urls import path
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse_lazy
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
    login_view,
    cadastro_paciente,
    logout_view,
    empresa_acesso,
    empresa_nova,
    empresas_lista,
    empresa_editar,
    empresa_excluir,
    esqueci_senha,
)

urlpatterns = [
    path("", home, name="home"),
    path("login/", login_view, name="login"),
    path("esqueci-senha/", esqueci_senha, name="esqueci_senha"),
    path(
        "redefinir-senha/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="registration/redefinir_senha.html",
            success_url=reverse_lazy("login"),
        ),
        name="redefinir_senha",
    ),
    path("sair/", logout_view, name="logout"),
    path("cadastro/", cadastro_paciente, name="cadastro_paciente"),
    path("empresas/", empresas_lista, name="empresas_lista"),
    path("empresas/cadastro/", empresa_nova, name="empresa_nova"),
    path("empresas/<int:pk>/editar/", empresa_editar, name="empresa_editar"),
    path("empresas/<int:pk>/excluir/", empresa_excluir, name="empresa_excluir"),
    path("<str:slug>/", empresa_acesso, name="empresa_acesso"),
    path("grupos/", grupos_lista, name="grupos_lista"),
    path("grupos/novo/", grupo_novo, name="grupo_novo"),
    path("grupos/<int:pk>/editar/", grupo_editar, name="grupo_editar"),
    path("grupos/<int:pk>/excluir/", grupo_excluir, name="grupo_excluir"),
    path("usuarios/", usuarios_lista, name="usuarios_lista"),
    path("usuarios/novo/", usuario_novo, name="usuario_novo"),
    path("usuarios/<int:pk>/editar/", usuario_editar, name="usuario_editar"),
    path("usuarios/<int:pk>/excluir/", usuario_excluir, name="usuario_excluir"),
]
