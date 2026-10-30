from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth import get_user_model

from .models import Empresa

User = get_user_model()


class EmpresaInline(admin.StackedInline):
    model = Empresa
    extra = 0
    readonly_fields = ("identificador_hash",)
    fieldsets = (
        ("Identificação e acesso", {"fields": ("identificador_hash", "usuario", ("razao_social", "nome_fantasia"), ("cnpj", "inscricao_estadual"))}),
        ("Contato", {"fields": (("email", "telefone"), "website", ("responsavel_nome", "responsavel_cargo"))}),
        ("Endereço", {"fields": (("cep", "estado"), ("logradouro", "numero", "complemento"), ("bairro", "cidade"))}),
        ("Licença", {"fields": (("plano_licenca", "status_licenca"), ("inicio_licenca", "fim_licenca"), "observacoes")}),
    )


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ("razao_social", "identificador_hash", "cnpj", "usuario", "plano_licenca", "status_licenca", "inicio_licenca", "fim_licenca")
    list_filter = ("plano_licenca", "status_licenca", "estado")
    search_fields = ("identificador_hash", "razao_social", "nome_fantasia", "cnpj", "email", "responsavel_nome", "usuario__username", "usuario__email")
    list_select_related = ("usuario",)
    date_hierarchy = "fim_licenca"
    ordering = ("razao_social",)
    readonly_fields = ("identificador_hash", "criado_em", "atualizado_em")
    fieldsets = EmpresaInline.fieldsets
    actions = ("ativar_licencas", "suspender_licencas")

    @admin.action(description="Ativar licenças selecionadas")
    def ativar_licencas(self, request, queryset):
        queryset.update(status_licenca=Empresa.StatusLicenca.ATIVA)

    @admin.action(description="Suspender licenças selecionadas")
    def suspender_licencas(self, request, queryset):
        queryset.update(status_licenca=Empresa.StatusLicenca.SUSPENSA)


try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    inlines = (EmpresaInline,)
    fieldsets = DjangoUserAdmin.fieldsets + (("Vínculo com a empresa", {"fields": ("empresa",)}),)
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (("Vínculo com a empresa", {"fields": ("empresa",)}),)
    list_display = ("username", "email", "first_name", "last_name", "tipo", "empresa", "is_staff", "empresa_vinculada")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "first_name", "last_name", "email", "empresa__razao_social")

    @admin.display(boolean=True, description="Empresa vinculada")
    def empresa_vinculada(self, obj):
        return obj.empresas.exists()
