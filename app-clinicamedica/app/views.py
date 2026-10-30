from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, redirect, render
from .forms import GrupoForm, LoginForm, PacienteCadastroForm, UsuarioCreateForm, UsuarioUpdateForm
from .models import Empresa

User = get_user_model()


def home(request):
    if not request.user.is_authenticated:
        return redirect("login")

    empresa = None

    if request.session.get("empresa_id"):
        empresa = Empresa.objects.filter(
            pk=request.session["empresa_id"],
            usuario=request.user
        ).first()
    dados = {"empresa": empresa}
    return render(request, "home.html", dados)


def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if form.is_valid():
        usuario = form.get_user()
        login(request, usuario)
        empresa = usuario.empresas.first()
        if empresa:
            request.session["empresa_id"] = empresa.pk
        return redirect("home")
    dados = {"form": form}
    return render(request, "login.html", dados)


def cadastro_paciente(request):
    form = PacienteCadastroForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("login")
    return render(request, "cadastro.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@staff_member_required
def usuarios_lista(request):
    busca = request.GET.get("busca", "").strip()
    donos = Empresa.objects.values_list("usuario_id", flat=True)
    usuarios = User.objects.exclude(pk__in=donos).exclude(is_superuser=True).order_by("username")
    if busca:
        usuarios = (
            usuarios.filter(username__icontains=busca)
            | usuarios.filter(first_name__icontains=busca)
            | usuarios.filter(last_name__icontains=busca)
            | usuarios.filter(email__icontains=busca)
        )
    dados = {"usuarios": usuarios, "busca": busca}
    return render(request, "usuarios/lista.html", dados)


@staff_member_required
def usuario_novo(request):
    form = UsuarioCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("usuarios_lista")
    dados = {"form": form, "titulo": "Novo usuário"}
    return render(request, "usuarios/form.html", dados)


@staff_member_required
def usuario_editar(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    form = UsuarioUpdateForm(request.POST or None, instance=usuario)
    if form.is_valid():
        form.save()
        return redirect("usuarios_lista")
    dados = {"form": form, "titulo": "Editar usuário", "usuario": usuario}
    return render(request, "usuarios/form.html", dados)


@staff_member_required
def usuario_excluir(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        usuario.delete()
        return redirect("usuarios_lista")
    dados = {"usuario": usuario}
    return render(request, "usuarios/excluir.html", dados)


@staff_member_required
def grupos_lista(request):
    grupos = Group.objects.prefetch_related("permissions").order_by("name")
    dados = {"grupos": grupos}
    return render(request, "grupos/lista.html", dados)


@staff_member_required
def grupo_novo(request):
    form = GrupoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("grupos_lista")
    dados = {"form": form, "titulo": "Novo grupo"}
    return render(request, "grupos/form.html", dados)


@staff_member_required
def grupo_editar(request, pk):
    grupo = get_object_or_404(Group, pk=pk)
    form = GrupoForm(request.POST or None, instance=grupo)
    if form.is_valid():
        form.save()
        return redirect("grupos_lista")
    dados = {"form": form, "titulo": "Editar grupo", "grupo": grupo}
    return render(request, "grupos/form.html", dados)


@staff_member_required
def grupo_excluir(request, pk):
    grupo = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        grupo.delete()
        return redirect("grupos_lista")
    dados = {"grupo": grupo}
    return render(request, "grupos/excluir.html", dados)
