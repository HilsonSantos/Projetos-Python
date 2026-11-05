from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def vincular_por_email_existente(apps, schema_editor):
    Paciente = apps.get_model("app", "Paciente")
    Usuario = apps.get_model("app", "Usuario")
    for paciente in Paciente.objects.filter(usuario__isnull=True).exclude(email="").iterator():
        contas = Usuario.objects.filter(
            empresa_id=paciente.empresa_id,
            tipo="P",
            email__iexact=paciente.email,
        )
        ids = list(contas.values_list("pk", flat=True)[:2])
        if len(ids) == 1:
            Paciente.objects.filter(pk=paciente.pk, usuario__isnull=True).update(usuario_id=ids[0])


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0018_convenio"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="usuario",
            name="cpf",
            field=models.CharField(blank=True, max_length=14, null=True, unique=True, verbose_name="CPF"),
        ),
        migrations.AddField(
            model_name="paciente",
            name="usuario",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="cadastros_paciente", to=settings.AUTH_USER_MODEL, verbose_name="conta de acesso"),
        ),
        migrations.RunPython(vincular_por_email_existente, migrations.RunPython.noop),
    ]
