import django.contrib.auth.models
import django.contrib.auth.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [("auth", "0012_alter_user_first_name_max_length")]

    operations = [
        migrations.CreateModel(
            name="Usuario",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                ("is_superuser", models.BooleanField(default=False, help_text="Designates that this user has all permissions without explicitly assigning them.", verbose_name="superuser status")),
                ("username", models.CharField(error_messages={"unique": "A user with that username already exists."}, help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.", max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name="username")),
                ("first_name", models.CharField(blank=True, max_length=150, verbose_name="first name")),
                ("last_name", models.CharField(blank=True, max_length=150, verbose_name="last name")),
                ("email", models.EmailField(blank=True, max_length=254, verbose_name="email address")),
                ("is_staff", models.BooleanField(default=False, help_text="Designates whether the user can log into this admin site.", verbose_name="staff status")),
                ("is_active", models.BooleanField(default=True, help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.", verbose_name="active")),
                ("date_joined", models.DateTimeField(default=django.utils.timezone.now, verbose_name="date joined")),
                ("groups", models.ManyToManyField(blank=True, help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.", related_name="user_set", related_query_name="user", to="auth.group", verbose_name="groups")),
                ("user_permissions", models.ManyToManyField(blank=True, help_text="Specific permissions for this user.", related_name="user_set", related_query_name="user", to="auth.permission", verbose_name="user permissions")),
            ],
            options={"db_table": "app_usuario", "swappable": "AUTH_USER_MODEL", "verbose_name": "usuário", "verbose_name_plural": "usuários"},
            managers=[("objects", django.contrib.auth.models.UserManager())],
        ),
        migrations.CreateModel(
            name="Empresa",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("razao_social", models.CharField(max_length=150, verbose_name="razão social")),
                ("nome_fantasia", models.CharField(blank=True, max_length=150, verbose_name="nome fantasia")),
                ("cnpj", models.CharField(max_length=18, unique=True, verbose_name="CNPJ")),
                ("inscricao_estadual", models.CharField(blank=True, max_length=30, verbose_name="inscrição estadual")),
                ("email", models.EmailField(max_length=254, unique=True, verbose_name="e-mail")),
                ("telefone", models.CharField(max_length=20)),
                ("website", models.URLField(blank=True, verbose_name="site")),
                ("responsavel_nome", models.CharField(max_length=150, verbose_name="responsável")),
                ("responsavel_cargo", models.CharField(blank=True, max_length=100, verbose_name="cargo do responsável")),
                ("cep", models.CharField(max_length=9)),
                ("logradouro", models.CharField(max_length=150)),
                ("numero", models.CharField(max_length=20)),
                ("complemento", models.CharField(blank=True, max_length=100)),
                ("bairro", models.CharField(max_length=100)),
                ("cidade", models.CharField(max_length=100)),
                ("estado", models.CharField(max_length=2)),
                ("plano_licenca", models.CharField(choices=[("basico", "Básico"), ("profissional", "Profissional"), ("empresarial", "Empresarial")], default="basico", max_length=20, verbose_name="plano da licença")),
                ("status_licenca", models.CharField(choices=[("pendente", "Pendente"), ("ativa", "Ativa"), ("suspensa", "Suspensa"), ("cancelada", "Cancelada"), ("expirada", "Expirada")], default="pendente", max_length=20, verbose_name="status da licença")),
                ("inicio_licenca", models.DateField(blank=True, null=True, verbose_name="início da licença")),
                ("fim_licenca", models.DateField(blank=True, null=True, verbose_name="fim da licença")),
                ("observacoes", models.TextField(blank=True, verbose_name="observações")),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
                ("atualizado_em", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "empresa",
                "verbose_name_plural": "empresas",
                "ordering": ["razao_social"],
            },
        ),
    ]
