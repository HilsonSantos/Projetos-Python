from functools import wraps

from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from .forms import GrupoForm, LoginForm, PacienteCadastroForm, UsuarioCreateForm, UsuarioUpdateForm
from .models import Empresa

User = get_user_model()


def administrador_required(view_func):
    """Permite a tela apenas a administradores, não apenas a usuários staff."""
    @wraps(view_func)
    @login_required
    def wrapped(request, *args, **kwargs):
        if not request.user.is_administrador:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return wrapped


def administrador_ou_colaborador_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapped(request, *args, **kwargs):
        if not (request.user.is_administrador or request.user.is_colaborador):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)

    return wrapped


def home(request):
    if not request.user.is_authenticated:
        return redirect("login")

    empresa = None

    if request.session.get("empresa_id"):
        empresa = Empresa.objects.filter(pk=request.session["empresa_id"]).first()
    dados = {"empresa": empresa}
    return render(request, "home.html", dados)


def empresa_acesso(request, identificador_hash):
    """Seleciona a empresa a partir do identificador público presente na URL."""
    # O hash é o endereço público; o ID numérico também é aceito para facilitar
    # testes e links antigos, mas não é exibido como identificador oficial.
    empresa = Empresa.objects.filter(identificador_hash__iexact=identificador_hash).first()
    if empresa is None and identificador_hash.isdigit():
        empresa = Empresa.objects.filter(pk=identificador_hash).first()
    if empresa is None:
        raise Http404("A empresa informada não existe ou não está cadastrada.")
    request.session["empresa_id"] = empresa.pk
    request.session["empresa_hash"] = empresa.identificador_hash
    return redirect("home" if request.user.is_authenticated else "login")


def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if form.is_valid():
        usuario = form.get_user()
        login(request, usuario)
        # Administradores têm acesso global. Os demais perfis são vinculados
        # automaticamente à empresa cadastrada no próprio usuário.
        if not usuario.is_administrador:
            empresa = usuario.empresa or usuario.empresas.first()
            if empresa:
                request.session["empresa_id"] = empresa.pk
                request.session["empresa_hash"] = empresa.identificador_hash
            else:
                request.session.pop("empresa_id", None)
                request.session.pop("empresa_hash", None)
        return redirect("home")
    dados = {"form": form}
    return render(request, "login.html", dados)


def cadastro_paciente(request):
    form = PacienteCadastroForm(request.POST or None)
    if form.is_valid():
        usuario = form.save(commit=False)
        empresa_id = request.session.get("empresa_id")
        if empresa_id:
            usuario.empresa_id = empresa_id
        usuario.save()
        return redirect("login")
    return render(request, "cadastro.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@administrador_ou_colaborador_required
def usuarios_lista(request):
    busca = request.GET.get("busca", "").strip()
    donos = Empresa.objects.values_list("usuario_id", flat=True)
    usuarios = User.objects.exclude(pk__in=donos).exclude(is_superuser=True).order_by("username")
    usuarios = User.objects.all().order_by("username")

    if not request.user.is_administrador:
        if request.user.empresa_id:
            usuarios = usuarios.filter(empresa_id=request.user.empresa_id)
        else:
            usuarios = usuarios.none()

    if busca:
        usuarios = (
            usuarios.filter(username__icontains=busca)
            | usuarios.filter(first_name__icontains=busca)
            | usuarios.filter(last_name__icontains=busca)
            | usuarios.filter(email__icontains=busca)
        )
    dados = {"usuarios": usuarios, "busca": busca}
    return render(request, "usuarios/lista.html", dados)


@administrador_required
def usuario_novo(request):
    form = UsuarioCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("usuarios_lista")
    dados = {"form": form, "titulo": "Novo usuário"}
    return render(request, "usuarios/form.html", dados)


@administrador_required
def usuario_editar(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    form = UsuarioUpdateForm(request.POST or None, instance=usuario)
    if form.is_valid():
        form.save()
        return redirect("usuarios_lista")
    dados = {"form": form, "titulo": "Editar usuário", "usuario": usuario}
    return render(request, "usuarios/form.html", dados)


@administrador_required
def usuario_excluir(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        usuario.delete()
        return redirect("usuarios_lista")
    dados = {"usuario": usuario}
    return render(request, "usuarios/excluir.html", dados)


@administrador_required
def grupos_lista(request):
    grupos = Group.objects.prefetch_related("permissions").order_by("name")
    dados = {"grupos": grupos}
    return render(request, "grupos/lista.html", dados)


@administrador_required
def grupo_novo(request):
    form = GrupoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("grupos_lista")
    dados = {"form": form, "titulo": "Novo grupo"}
    return render(request, "grupos/form.html", dados)


@administrador_required
def grupo_editar(request, pk):
    grupo = get_object_or_404(Group, pk=pk)
    form = GrupoForm(request.POST or None, instance=grupo)
    if form.is_valid():
        form.save()
        return redirect("grupos_lista")
    dados = {"form": form, "titulo": "Editar grupo", "grupo": grupo}
    return render(request, "grupos/form.html", dados)


@administrador_required
def grupo_excluir(request, pk):
    grupo = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        grupo.delete()
        return redirect("grupos_lista")
    dados = {"grupo": grupo}
    return render(request, "grupos/excluir.html", dados)
