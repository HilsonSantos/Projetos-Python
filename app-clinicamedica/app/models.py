import hashlib
import re
import uuid
import unicodedata
from django.db.models import Q

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

    class Profissao(models.TextChoices):
        MEDICO = "MED", "Médico(a)"
        RECEPCIONISTA = "REC", "Recepcionista"
        ENFERMEIRO = "ENF", "Enfermeiro(a)"
        TECNICO_ENFERMAGEM = "TENF", "Técnico(a) de enfermagem"
        PSICOLOGO = "PSI", "Psicólogo(a)"
        FISIOTERAPEUTA = "FIS", "Fisioterapeuta"
        DENTISTA = "DEN", "Dentista"
        NUTRICIONISTA = "NUT", "Nutricionista"
        FARMACEUTICO = "FAR", "Farmacêutico(a)"
        OUTRO = "OUT", "Outro"

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
    cpf = models.CharField("CPF", max_length=14, unique=True, null=True, blank=True)
    telefone = models.CharField("telefone", max_length=20, blank=True)
    whatsapp = models.CharField("WhatsApp", max_length=20, blank=True)
    profissao = models.CharField("tipo de profissional", max_length=10, choices=Profissao.choices, blank=True)

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

    def save(self, *args, **kwargs):
        self.cpf = re.sub(r"\D", "", self.cpf or "") or None
        super().save(*args, **kwargs)
        if self.tipo == self.Tipo.PACIENTE:
            vincular_usuario_a_paciente(self)

    @property
    def pode_gerenciar_usuarios_grupos(self):
        dono_app = self.is_superuser and self.tipo == self.Tipo.ADMINISTRADOR
        colaborador_autorizado = self.tipo == self.Tipo.COLABORADOR and self.is_staff
        return dono_app or colaborador_autorizado

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


class Paciente(models.Model):
    class Sexo(models.TextChoices):
        FEMININO = "F", "Feminino"
        MASCULINO = "M", "Masculino"
        OUTRO = "O", "Outro"
        NAO_INFORMADO = "N", "Prefiro não informar"

    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="pacientes")
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="cadastros_paciente",
        null=True,
        blank=True,
        verbose_name="conta de acesso",
    )
    nome_completo = models.CharField("nome completo", max_length=200)
    cpf = models.CharField("CPF", max_length=14)
    data_nascimento = models.DateField("data de nascimento")
    sexo = models.CharField("sexo", max_length=1, choices=Sexo.choices, blank=True)
    telefone = models.CharField("telefone", max_length=20)
    whatsapp = models.CharField("WhatsApp", max_length=20, blank=True)
    email = models.EmailField("e-mail", blank=True)
    cep = models.CharField("CEP", max_length=9)
    logradouro = models.CharField("logradouro", max_length=150)
    numero = models.CharField("número", max_length=20)
    complemento = models.CharField("complemento", max_length=100, blank=True)
    bairro = models.CharField("bairro", max_length=100)
    cidade = models.CharField("cidade", max_length=100)
    estado = models.CharField("UF", max_length=2)
    contato_emergencia_nome = models.CharField("nome do contato de emergência", max_length=150, blank=True)
    contato_emergencia_telefone = models.CharField("telefone de emergência", max_length=20, blank=True)
    convenio = models.ForeignKey(
        "Convenio",
        on_delete=models.SET_NULL,
        related_name="pacientes",
        null=True,
        blank=True,
        verbose_name="convênio",
    )
    numero_carteirinha = models.CharField("número da carteirinha", max_length=50, blank=True)
    observacoes = models.TextField("observações", blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "pacientes"
        ordering = ["nome_completo"]
        constraints = [
            models.UniqueConstraint(fields=["empresa", "cpf"], name="uniq_paciente_cpf_empresa"),
        ]
        verbose_name = "paciente"
        verbose_name_plural = "pacientes"

    def __str__(self):
        return self.nome_completo

    def save(self, *args, **kwargs):
        self.cpf = re.sub(r"\D", "", self.cpf or "")
        super().save(*args, **kwargs)
        if not self.usuario_id:
            vincular_paciente_a_usuario(self)


class Convenio(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="convenios")
    nome = models.CharField("nome do convênio", max_length=150)
    registro_ans = models.CharField("registro ANS", max_length=20, blank=True)
    telefone = models.CharField("telefone de contato", max_length=20, blank=True)
    email = models.EmailField("e-mail de contato", blank=True)
    observacoes = models.TextField("cobertura e observações", blank=True)
    ativo = models.BooleanField("ativo", default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "convenios"
        ordering = ["nome"]
        constraints = [
            models.UniqueConstraint(fields=["empresa", "nome"], name="uniq_convenio_nome_empresa"),
        ]
        verbose_name = "convênio"
        verbose_name_plural = "convênios"

    def __str__(self):
        return self.nome


def vincular_usuario_a_paciente(usuario):
    if not usuario.empresa_id or not (usuario.cpf or usuario.email):
        return
    candidatos = Paciente.objects.filter(empresa_id=usuario.empresa_id, usuario__isnull=True)
    correspondencias = Q()
    if usuario.cpf:
        correspondencias |= Q(cpf=usuario.cpf)
    if usuario.email:
        correspondencias |= Q(email__iexact=usuario.email)
    ids = list(candidatos.filter(correspondencias).values_list("pk", flat=True)[:2])
    if len(ids) == 1:
        Paciente.objects.filter(pk=ids[0], usuario__isnull=True).update(usuario_id=usuario.pk)


def vincular_paciente_a_usuario(paciente):
    correspondencias = Q()
    if paciente.cpf:
        correspondencias |= Q(cpf=paciente.cpf)
    if paciente.email:
        correspondencias |= Q(email__iexact=paciente.email)
    if not correspondencias:
        return
    candidatos = Usuario.objects.filter(
        empresa_id=paciente.empresa_id,
        tipo=Usuario.Tipo.PACIENTE,
    ).filter(correspondencias)
    ids = [
        usuario.pk for usuario in candidatos
        if not usuario.cadastros_paciente.filter(empresa_id=paciente.empresa_id).exists()
    ][:2]
    if len(ids) == 1:
        Paciente.objects.filter(pk=paciente.pk, usuario__isnull=True).update(usuario_id=ids[0])
