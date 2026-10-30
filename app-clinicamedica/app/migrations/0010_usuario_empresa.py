from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("app", "0009_normalize_usuario_tipo")]

    operations = [
        migrations.AddField(
            model_name="usuario",
            name="empresa",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="usuarios",
                to="app.empresa",
                verbose_name="empresa",
            ),
        ),
    ]
