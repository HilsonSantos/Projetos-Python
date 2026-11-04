from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("app", "0014_usuario_telefone")]

    operations = [
        migrations.AlterField(
            model_name="usuario",
            name="telefone",
            field=models.CharField(blank=True, max_length=20, verbose_name="telefone"),
        ),
        migrations.AddField(
            model_name="usuario",
            name="whatsapp",
            field=models.CharField(blank=True, max_length=20, verbose_name="WhatsApp"),
        ),
    ]
