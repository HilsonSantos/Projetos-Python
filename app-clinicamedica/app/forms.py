from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm
from .models import Empresa

User = get_user_model()

class LoginForm(AuthenticationForm):
    empresa = forms.CharField(
        label="Link ou identificador da empresa",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "clinicamedica0001"}),
    )


class EsqueciSenhaForm(forms.Form):
    empresa = forms.CharField(
        label="Link ou identificador da empresa",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "clinicamedica0001"}),
    )
    username = forms.CharField(label="Usuário", widget=forms.TextInput(attrs={"class": "form-control"}))


class EmpresaCadastroForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = (
            "razao_social", "nome_fantasia", "cnpj", "inscricao_estadual",
            "email", "telefone", "website", "responsavel_nome", "responsavel_cargo",
            "cep", "logradouro", "numero", "complemento", "bairro", "cidade", "estado",
            "plano_licenca", "status_licenca", "inicio_licenca", "fim_licenca", "observacoes",
        )
        widgets = {
            "inicio_licenca": forms.DateInput(attrs={"type": "date"}),
            "fim_licenca": forms.DateInput(attrs={"type": "date"}),
            "observacoes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class PacienteCadastroForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "telefone", "whatsapp")
        labels = {"username": "Usuário", "first_name": "Nome", "last_name": "Sobrenome", "email": "E-mail", "telefone": "Telefone", "whatsapp": "WhatsApp"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.tipo = User.Tipo.PACIENTE
        usuario.is_staff = False
        usuario.is_superuser = False
        if commit:
            usuario.save()
        return usuario


def rotulo_permissao(permissao):
    acoes = {
        "add": "Adicionar",
        "change": "Alterar",
        "delete": "Excluir",
        "view": "Visualizar",
    }
    acao, _, _ = permissao.codename.partition("_")
    modelo = permissao.content_type.model_class()
    nomes_modelos = {"user": "Usuário", "group": "Grupo", "permission": "Permissão"}
    nome_modelo = nomes_modelos.get(
        permissao.content_type.model,
        modelo._meta.verbose_name.title() if modelo else permissao.content_type.name.title(),
    )
    return f"{acoes.get(acao, acao.title())} {nome_modelo}"


class UsuarioCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._aplicar_bootstrap()

    def _aplicar_bootstrap(self):
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-check-input" if isinstance(field.widget, forms.CheckboxInput) else "form-control"
        self.fields["user_permissions"].label_from_instance = rotulo_permissao

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.is_staff = usuario.tipo == User.Tipo.ADMINISTRADOR or usuario.is_superuser
        if commit:
            usuario.save()
            self.save_m2m()
        return usuario

    def clean(self):
        cleaned_data = super().clean()
        if (
            "empresa" in self.fields
            and
            cleaned_data.get("tipo") != User.Tipo.ADMINISTRADOR
            and not cleaned_data.get("empresa")
        ):
            self.add_error("empresa", "Informe a empresa para este tipo de usuário.")
        if cleaned_data.get("tipo") == User.Tipo.COLABORADOR and not cleaned_data.get("profissao"):
            self.add_error("profissao", "Informe o tipo de profissional do colaborador.")
        return cleaned_data

    class Meta:
        model = User
        fields = (
            "username", "first_name", "last_name", "email", "telefone", "whatsapp", "tipo", "profissao", "empresa", "is_active",
            "is_staff", "is_superuser", "groups", "user_permissions",
        )


class UsuarioUpdateForm(forms.ModelForm):
    nova_senha = forms.CharField(label="Nova senha", required=False, widget=forms.PasswordInput)
    confirmar_senha = forms.CharField(label="Confirmar nova senha", required=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            "username", "first_name", "last_name", "email", "telefone", "whatsapp", "tipo", "profissao", "empresa", "is_active",
            "is_staff", "is_superuser", "groups", "user_permissions",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs["class"] = "form-check-input"
            elif isinstance(field.widget, forms.SelectMultiple):
                field.widget.attrs["class"] = "form-select"
                field.widget.attrs["size"] = 8
            else:
                field.widget.attrs["class"] = "form-control"
        self.fields["user_permissions"].label_from_instance = rotulo_permissao

    def clean(self):
        cleaned_data = super().clean()
        if (
            "empresa" in self.fields
            and
            cleaned_data.get("tipo") != User.Tipo.ADMINISTRADOR
            and not cleaned_data.get("empresa")
        ):
            self.add_error("empresa", "Informe a empresa para este tipo de usuário.")
        if cleaned_data.get("tipo") == User.Tipo.COLABORADOR and not cleaned_data.get("profissao"):
            self.add_error("profissao", "Informe o tipo de profissional do colaborador.")
        senha = cleaned_data.get("nova_senha")
        confirmacao = cleaned_data.get("confirmar_senha")
        if senha != confirmacao:
            self.add_error("confirmar_senha", "As senhas não conferem.")
        return cleaned_data

    def save(self, commit=True):
        usuario = super().save(commit=False)
        # O tipo define o acesso; as flags do Django acompanham o papel.
        usuario.is_staff = usuario.tipo == User.Tipo.ADMINISTRADOR or usuario.is_superuser
        if self.cleaned_data.get("nova_senha"):
            usuario.set_password(self.cleaned_data["nova_senha"])
        if commit:
            usuario.save()
        return usuario


class GrupoForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ("name", "permissions")
        labels = {"name": "Nome do grupo", "permissions": "Permissões"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].widget.attrs["class"] = "form-control"
        self.fields["permissions"].widget.attrs.update({"class": "form-select", "size": 12})
        self.fields["permissions"].label_from_instance = rotulo_permissao
