from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0001_empresa"),
    ]

    operations = [
        migrations.AddField(
            model_name="empresa",
            name="usuario",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="empresa",
                to=settings.AUTH_USER_MODEL,
                verbose_name="usuário do Django",
            ),
        ),
    ]
