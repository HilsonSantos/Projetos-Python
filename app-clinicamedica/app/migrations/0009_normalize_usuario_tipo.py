from django.db import migrations, models


def normalizar_tipos(apps, schema_editor):
    Usuario = apps.get_model("app", "Usuario")
    Usuario.objects.filter(tipo="ADMINISTRADOR").update(tipo="A")
    Usuario.objects.filter(tipo="COLABORADOR").update(tipo="C")
    Usuario.objects.filter(tipo="PACIENTE").update(tipo="P")


def restaurar_tipos(apps, schema_editor):
    Usuario = apps.get_model("app", "Usuario")
    Usuario.objects.filter(tipo="A").update(tipo="ADMINISTRADOR")
    Usuario.objects.filter(tipo="C").update(tipo="COLABORADOR")
    Usuario.objects.filter(tipo="P").update(tipo="PACIENTE")


class Migration(migrations.Migration):
    dependencies = [("app", "0008_usuario_tipo")]

    operations = [
        migrations.RunPython(normalizar_tipos, restaurar_tipos),
        migrations.AlterField(
            model_name="usuario",
            name="tipo",
            field=models.CharField(
                choices=[
                    ("A", "Administrador"),
                    ("C", "Colaborador"),
                    ("P", "Paciente"),
                ],
                default="P",
                max_length=20,
                verbose_name="tipo de usuário",
            ),
        ),
    ]
