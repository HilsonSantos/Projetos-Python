from django.db import migrations


def promover_administradores_legados(apps, schema_editor):
    Usuario = apps.get_model("app", "Usuario")
    Usuario.objects.filter(is_staff=True).update(tipo="A")
    Usuario.objects.filter(is_superuser=True).update(tipo="A", is_staff=True)


class Migration(migrations.Migration):
    dependencies = [("app", "0010_usuario_empresa")]

    operations = [migrations.RunPython(promover_administradores_legados, migrations.RunPython.noop)]
