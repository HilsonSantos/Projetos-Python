import hashlib
import re
import uuid
import unicodedata

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


def gerar_identificador_hash():
    """Gera um identificador público que não expõe dados da empresa."""
    return hashlib.sha256(uuid.uuid4().bytes).hexdigest()


def gerar_slug_empresa(nome):
    nome_normalizado = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]", "", nome_normalizado.lower())


class Usuario(AbstractUser):
    """Usuário da aplicação, armazenado na tabela usuarios."""

    class Tipo(models.TextChoices):
        ADMINISTRADOR = "A", "Administrador"
        COLABORADOR = "C", "Colaborador"
        PACIENTE = "P", "Paciente"

    tipo = models.CharField(
        "tipo de usuário",
        max_length=20,
        choices=Tipo.choices,
        default=Tipo.PACIENTE,
    )
    empresa = models.ForeignKey(
        "Empresa",
        on_delete=models.SET_NULL,
        related_name="usuarios",
        null=True,
        blank=True,
        verbose_name="empresa",
    )
    telefone = models.CharField("telefone", max_length=20, blank=True)
    whatsapp = models.CharField("WhatsApp", max_length=20, blank=True)

    @property
    def is_administrador(self):
        """Indica se o usuário pode administrar a aplicação."""
        return self.is_superuser or self.tipo == self.Tipo.ADMINISTRADOR

    @property
    def is_colaborador(self):
        return self.tipo == self.Tipo.COLABORADOR

    @property
    def is_paciente(self):
        return self.tipo == self.Tipo.PACIENTE

    class Meta:
        db_table = "usuarios"
        swappable = "AUTH_USER_MODEL"
        verbose_name = "usuário"
        verbose_name_plural = "usuários"


class Empresa(models.Model):
    class StatusLicenca(models.TextChoices):
        PENDENTE = "P", "Pendente"
        ATIVA = "A", "Ativa"
        SUSPENSA = "S", "Suspensa"
        CANCELADA = "C", "Cancelada"
        EXPIRADA = "E", "Expirada"

    class PlanoLicenca(models.TextChoices):
        BASICO = "B", "Básico"
        PROFISSIONAL = "P", "Profissional"
        EMPRESARIAL = "E", "Empresarial"

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="empresas",
        null=True,
        blank=True,
        verbose_name="usuário",
    )
    identificador_hash = models.CharField(
        "identificador hash",
        max_length=64,
        unique=True,
        editable=False,
        default=gerar_identificador_hash,
        help_text="Identificador público e permanente da empresa.",
    )
    slug = models.SlugField("nome para acesso", max_length=180, unique=True, blank=True)
    razao_social = models.CharField("razão social", max_length=200)
    nome_fantasia = models.CharField("nome fantasia", max_length=150, blank=True)
    cnpj = models.CharField("CNPJ", max_length=18, unique=True)
    inscricao_estadual = models.CharField("inscrição estadual", max_length=30, blank=True)
    email = models.EmailField("e-mail", unique=True)
    telefone = models.CharField(max_length=20)
    website = models.URLField("site", blank=True)
    responsavel_nome = models.CharField("responsável", max_length=150)
    responsavel_cargo = models.CharField("cargo do responsável", max_length=100, blank=True)
    cep = models.CharField(max_length=9)
    logradouro = models.CharField(max_length=150)
    numero = models.CharField(max_length=20)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)
    plano_licenca = models.CharField(
        "plano da licença",
        max_length=20,
        choices=PlanoLicenca.choices,
        default=PlanoLicenca.BASICO
    )
    status_licenca = models.CharField(
        "status da licença",
        max_length=20,
        choices=StatusLicenca.choices,
        default=StatusLicenca.PENDENTE
    )
    inicio_licenca = models.DateField("início da licença", null=True, blank=True)
    fim_licenca = models.DateField("fim da licença", null=True, blank=True)
    observacoes = models.TextField("observações", blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = gerar_slug_empresa(self.nome_fantasia or self.razao_social) or "clinica"
            slug = base_slug
            sufixo = 2
            while Empresa.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                slug = f"{base_slug}-{sufixo}"
                sufixo += 1
            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        db_table = "empresas"
        ordering = ["razao_social"]
        verbose_name = "empresa"
        verbose_name_plural = "empresas"

    def __str__(self):
        return self.nome_fantasia or self.razao_social
