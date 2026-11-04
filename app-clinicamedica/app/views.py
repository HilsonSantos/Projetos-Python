from functools import wraps
import re
from urllib.parse import urlencode, urlparse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.urls import reverse
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from .forms import EmpresaCadastroForm, EsqueciSenhaForm, GrupoForm, LoginForm, PacienteCadastroForm, UsuarioCreateForm, UsuarioUpdateForm
from .models import Empresa
from .whatsapp import enviar_link_redefinicao, WhatsAppNaoConfigurado, FalhaEnvioWhatsApp

User = get_user_model()


def usuario_e_dono_app(usuario):
    return usuario.is_superuser and usuario.tipo == User.Tipo.ADMINISTRADOR


def administrador_required(view_func):
    """ Permite a tela apenas a administradores, não apenas a usuários staff. """
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


def dono_app_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapped(request, *args, **kwargs):
        if not usuario_e_dono_app(request.user):
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return wrapped

def home(request):
    if not request.user.is_authenticated:
        return redirect("login")

    empresa = None

    if request.session.get("empresa_id"):
        empresa = Empresa.objects.filter(pk=request.session["empresa_id"]).first()
        if (
            empresa
            and not usuario_e_dono_app(request.user)
            and request.user.empresa_id != empresa.pk
            and empresa.usuario_id != request.user.pk
        ):
            request.session.pop("empresa_id", None)
            request.session.pop("empresa_hash", None)
            request.session.pop("empresa_slug", None)
            empresa = None
    dados = {"empresa": empresa}
    return render(request, "home.html", dados)


@login_required
def empresa_nova(request):
    if not usuario_e_dono_app(request.user):
        raise PermissionDenied
    form = EmpresaCadastroForm(request.POST or None)
    if form.is_valid():
        empresa = form.save(commit=False)
        empresa.usuario = request.user
        empresa.save()
        return redirect("empresas_lista")
    return render(request, "empresas/form.html", {"form": form})


@login_required
def empresas_lista(request):
    if not usuario_e_dono_app(request.user):
        raise PermissionDenied
    empresas = Empresa.objects.select_related("usuario").order_by("razao_social")
    return render(request, "empresas/lista.html", {"empresas": empresas})


@login_required
def empresa_editar(request, pk):
    if not usuario_e_dono_app(request.user):
        raise PermissionDenied
    empresa = get_object_or_404(Empresa, pk=pk)
    form = EmpresaCadastroForm(request.POST or None, instance=empresa)
    if form.is_valid():
        form.save()
        return redirect("empresas_lista")
    return render(request, "empresas/form.html", {"form": form, "empresa": empresa})


@login_required
def empresa_excluir(request, pk):
    if not usuario_e_dono_app(request.user):
        raise PermissionDenied
    empresa = get_object_or_404(Empresa, pk=pk)
    if request.method == "POST":
        empresa.delete()
        return redirect("empresas_lista")
    return render(request, "empresas/excluir.html", {"empresa": empresa})


def empresa_acesso(request, slug):
    """Seleciona a empresa pelo nome legível ou por links antigos com hash."""
    empresa = Empresa.objects.filter(slug=slug).first()
    if empresa is None:
        empresa = Empresa.objects.filter(slug__iexact=slug).first()

    if empresa is None and slug.isdigit():
        empresa = Empresa.objects.filter(pk=slug).first()

    if empresa is None:
        raise Http404("A empresa informada não existe ou não está cadastrada.")

    if request.user.is_authenticated and not usuario_e_dono_app(request.user):
        pertence_empresa = (
            request.user.empresa_id == empresa.pk
            or empresa.usuario_id == request.user.pk
        )
        if not pertence_empresa:
            raise PermissionDenied("Este usuário não pertence à empresa selecionada.")

    request.session["empresa_id"] = empresa.pk
    request.session["empresa_slug"] = empresa.slug
    return redirect("home" if request.user.is_authenticated else "login")


def login_view(request):
    form = LoginForm(
        request,
        data=request.POST or None,
        initial={"empresa": request.session.get("empresa_slug", "")},
    )
    if form.is_valid():
        usuario = form.get_user()
        valor_empresa = form.cleaned_data["empresa"].strip()
        caminho = urlparse(valor_empresa if "://" in valor_empresa else f"/{valor_empresa.strip('/')}/").path
        identificador_empresa = caminho.rstrip("/").split("/")[-1]
        empresa = Empresa.objects.filter(slug__iexact=identificador_empresa).first()
        if empresa is None:
            form.add_error("empresa", "Não encontramos uma empresa com esse link ou identificador.")
            return render(request, "login.html", {"form": form})

        pertence_empresa = usuario.empresa_id == empresa.pk or empresa.usuario_id == usuario.pk
        if not usuario_e_dono_app(usuario) and not pertence_empresa:
            form.add_error(None, "Este usuário não pertence à empresa informada.")
            return render(request, "login.html", {"form": form})

        login(request, usuario)
        request.session["empresa_id"] = empresa.pk
        request.session["empresa_hash"] = empresa.identificador_hash
        request.session["empresa_slug"] = empresa.slug
        return redirect("home")
    dados = {"form": form}
    return render(request, "login.html", dados)


def cadastro_paciente(request):
    form = PacienteCadastroForm(request.POST or None)
    if form.is_valid():
        slug_empresa = request.session.get("empresa_slug")
        empresa = Empresa.objects.filter(slug__iexact=slug_empresa).first() if slug_empresa else None
        if empresa is None and request.session.get("empresa_id"):
            empresa = Empresa.objects.filter(pk=request.session["empresa_id"]).first()
        if empresa is None:
            form.add_error(None, "Informe o link da empresa antes de realizar o cadastro.")
            return render(request, "cadastro.html", {"form": form})

        usuario = form.save(commit=False)
        usuario.empresa = empresa
        usuario.telefone = form.cleaned_data.get("telefone", "").strip()
        usuario.whatsapp = form.cleaned_data.get("whatsapp", "").strip()
        usuario.save()
        request.session["empresa_id"] = empresa.pk
        request.session["empresa_slug"] = empresa.slug
        return redirect("login")
    return render(request, "cadastro.html", {"form": form})


def logout_view(request):
    slug_empresa = request.session.get("empresa_slug", "")
    if not slug_empresa and request.session.get("empresa_id"):
        slug_empresa = (
            Empresa.objects.filter(pk=request.session["empresa_id"])
            .values_list("slug", flat=True)
            .first()
            or ""
        )
    logout(request)
    if slug_empresa:
        request.session["empresa_slug"] = slug_empresa
    return redirect("login")


def esqueci_senha(request):
    form = EsqueciSenhaForm(
        request.POST or None,
        initial={"empresa": request.session.get("empresa_slug", "")},
    )
    enviado = False
    erro_envio = False
    processado = False
    if form.is_valid():
        processado = True
        valor = form.cleaned_data["empresa"].strip()
        caminho = urlparse(valor if "://" in valor else f"/{valor.strip('/')}/").path
        slug = caminho.rstrip("/").split("/")[-1]
        empresa = Empresa.objects.filter(slug__iexact=slug).first()
        usuario = User.objects.filter(username__iexact=form.cleaned_data["username"]).first()
        vinculado = usuario and empresa and (
            usuario.empresa_id == empresa.pk or empresa.usuario_id == usuario.pk
        )
        telefone = re.sub(r"\D", "", usuario.whatsapp or "") if vinculado else ""
        if telefone and len(telefone) in (10, 11):
            telefone = "55" + telefone
        if telefone and 10 <= len(telefone) <= 15:
            uid = urlsafe_base64_encode(force_bytes(usuario.pk))
            token = default_token_generator.make_token(usuario)
            reset_url = request.build_absolute_uri(
                reverse("redefinir_senha", kwargs={"uidb64": uid, "token": token})
                + "?"
                + urlencode({"empresa": empresa.slug})
            )
            try:
                enviar_link_redefinicao(telefone, reset_url)
                enviado = True
            except (WhatsAppNaoConfigurado, FalhaEnvioWhatsApp):
                erro_envio = True
        # A mesma resposta é mostrada para contas inexistentes, sem vínculo ou sem WhatsApp.
    return render(request, "registration/esqueci_senha.html", {
        "form": form, "enviado": enviado, "erro_envio": erro_envio, "processado": processado,
    })


@administrador_ou_colaborador_required
def usuarios_lista(request):
    empresa_id = request.session.get("empresa_id")
    busca = request.GET.get("busca", "").strip()
    usuarios = (
        User
        .objects
        .filter(Q(empresa_id=empresa_id) | Q(empresas__id=empresa_id))
        .distinct()

        if empresa_id else User.objects.none()
    )
    usuarios = usuarios.order_by("username")

    if busca:
        usuarios = (
            usuarios.filter(username__icontains=busca) |
            usuarios.filter(first_name__icontains=busca) |
            usuarios.filter(last_name__icontains=busca) |
            usuarios.filter(email__icontains=busca)
        )
    dados = {"usuarios": usuarios, "busca": busca}
    return render(request, "usuarios/lista.html", dados)


@administrador_ou_colaborador_required
def usuario_novo(request):
    form = UsuarioCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("usuarios_lista")
    dados = {"form": form, "titulo": "Novo usuário"}
    return render(request, "usuarios/form.html", dados)


@administrador_ou_colaborador_required
def usuario_editar(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    form = UsuarioUpdateForm(request.POST or None, instance=usuario)
    if form.is_valid():
        form.save()
        return redirect("usuarios_lista")
    dados = {"form": form, "titulo": "Editar usuário", "usuario": usuario}
    return render(request, "usuarios/form.html", dados)


@administrador_ou_colaborador_required
def usuario_excluir(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        usuario.delete()
        return redirect("usuarios_lista")
    dados = {"usuario": usuario}
    return render(request, "usuarios/excluir.html", dados)


@administrador_ou_colaborador_required
def grupos_lista(request):
    grupos = Group.objects.prefetch_related("permissions").order_by("name")
    dados = {"grupos": grupos}
    return render(request, "grupos/lista.html", dados)


@administrador_ou_colaborador_required
def grupo_novo(request):
    form = GrupoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("grupos_lista")
    dados = {"form": form, "titulo": "Novo grupo"}
    return render(request, "grupos/form.html", dados)


@administrador_ou_colaborador_required
def grupo_editar(request, pk):
    grupo = get_object_or_404(Group, pk=pk)
    form = GrupoForm(request.POST or None, instance=grupo)
    if form.is_valid():
        form.save()
        return redirect("grupos_lista")
    dados = {"form": form, "titulo": "Editar grupo", "grupo": grupo}
    return render(request, "grupos/form.html", dados)


@administrador_ou_colaborador_required
def grupo_excluir(request, pk):
    grupo = get_object_or_404(Group, pk=pk)
    if request.method == "POST":
        grupo.delete()
        return redirect("grupos_lista")
    dados = {"grupo": grupo}
    return render(request, "grupos/excluir.html", dados)
