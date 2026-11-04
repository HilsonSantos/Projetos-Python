import re
import unicodedata

from django.db import migrations, models


def gerar_slug(nome):
    normalizado = unicodedata.normalize("NFKD", nome).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", normalizado.lower())).strip("-") or "clinica"


def preencher_slugs(apps, schema_editor):
    Empresa = apps.get_model("app", "Empresa")
    for empresa in Empresa.objects.all().order_by("pk"):
        base = gerar_slug(empresa.nome_fantasia or empresa.razao_social)
        slug = base
        sufixo = 2
        while Empresa.objects.filter(slug=slug).exclude(pk=empresa.pk).exists():
            slug = f"{base}-{sufixo}"
            sufixo += 1
        Empresa.objects.filter(pk=empresa.pk).update(slug=slug)


class Migration(migrations.Migration):
    dependencies = [("app", "0012_rename_empresa_usuario_tables")]

    operations = [
        migrations.AddField(
            model_name="empresa",
            name="slug",
            field=models.SlugField(blank=True, max_length=180, null=True, unique=True, verbose_name="nome para acesso"),
        ),
        migrations.RunPython(preencher_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="empresa",
            name="slug",
            field=models.SlugField(blank=True, max_length=180, unique=True, verbose_name="nome para acesso"),
        ),
    ]
