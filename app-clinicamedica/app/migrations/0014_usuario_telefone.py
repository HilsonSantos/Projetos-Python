from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("app", "0013_empresa_slug")]

    operations = [
        migrations.AddField(
            model_name="usuario",
            name="telefone",
            field=models.CharField(blank=True, max_length=20, verbose_name="WhatsApp"),
        ),
    ]
