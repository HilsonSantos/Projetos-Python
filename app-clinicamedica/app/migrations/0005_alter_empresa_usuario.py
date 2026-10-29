from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0004_empresa_identificador_hash"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name="empresa",
                    name="usuario",
                    field=models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="empresas",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="usuário",
                    ),
                ),
            ],
            database_operations=[
                migrations.RunSQL(
                    "ALTER TABLE app_empresa ADD COLUMN IF NOT EXISTS usuario_id bigint;",
                    migrations.RunSQL.noop,
                ),
            ],
        ),
    ]
