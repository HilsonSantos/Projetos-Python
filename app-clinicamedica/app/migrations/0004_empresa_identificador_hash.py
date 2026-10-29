from django.db import migrations, models

import app.models


def preencher_identificadores_hash(apps, schema_editor):
    empresa_model = apps.get_model("app", "Empresa")
    with schema_editor.connection.cursor() as cursor:
        cursor.execute("SELECT id FROM app_empresa WHERE identificador_hash IS NULL")
        ids = [row[0] for row in cursor.fetchall()]
        for empresa_id in ids:
            cursor.execute(
                "UPDATE app_empresa SET identificador_hash = %s WHERE id = %s",
                [app.models.gerar_identificador_hash(), empresa_id],
            )


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0003_merge_20261026_2157"),
    ]

    operations = [
        migrations.AddField(
            model_name="empresa",
            name="identificador_hash",
            field=models.CharField(
                editable=False,
                help_text="Identificador público e permanente da empresa.",
                max_length=64,
                null=True,
                verbose_name="identificador hash",
            ),
        ),
        migrations.RunPython(
            code=preencher_identificadores_hash,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name="empresa",
            name="identificador_hash",
            field=models.CharField(
                default=app.models.gerar_identificador_hash,
                editable=False,
                help_text="Identificador público e permanente da empresa.",
                max_length=64,
                unique=True,
                verbose_name="identificador hash",
            ),
        ),
    ]
