from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("app", "0011_promote_legacy_admins")]

    operations = [
        migrations.AlterModelTable(
            name="empresa",
            table="empresas",
        ),
        migrations.AlterModelTable(
            name="usuario",
            table="usuarios",
        ),
    ]
