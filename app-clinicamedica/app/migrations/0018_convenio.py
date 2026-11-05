from django.db import migrations, models
import django.db.models.deletion


def migrar_convenios_existentes(apps, schema_editor):
    Paciente = apps.get_model("app", "Paciente")
    Convenio = apps.get_model("app", "Convenio")
    for paciente in Paciente.objects.exclude(convenio="").iterator():
        convenio, _ = Convenio.objects.get_or_create(
            empresa_id=paciente.empresa_id,
            nome=paciente.convenio,
        )
        Paciente.objects.filter(pk=paciente.pk).update(convenio_registro_id=convenio.pk)


class Migration(migrations.Migration):
    dependencies = [("app", "0017_paciente")]

    operations = [
        migrations.CreateModel(
            name="Convenio",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=150, verbose_name="nome do convênio")),
                ("registro_ans", models.CharField(blank=True, max_length=20, verbose_name="registro ANS")),
                ("telefone", models.CharField(blank=True, max_length=20, verbose_name="telefone de contato")),
                ("email", models.EmailField(blank=True, max_length=254, verbose_name="e-mail de contato")),
                ("observacoes", models.TextField(blank=True, verbose_name="cobertura e observações")),
                ("ativo", models.BooleanField(default=True, verbose_name="ativo")),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
                ("atualizado_em", models.DateTimeField(auto_now=True)),
                ("empresa", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="convenios", to="app.empresa")),
            ],
            options={
                "verbose_name": "convênio",
                "verbose_name_plural": "convênios",
                "db_table": "convenios",
                "ordering": ["nome"],
                "constraints": [models.UniqueConstraint(fields=("empresa", "nome"), name="uniq_convenio_nome_empresa")],
            },
        ),
        migrations.AddField(
            model_name="paciente",
            name="convenio_registro",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="pacientes_migracao", to="app.convenio"),
        ),
        migrations.RunPython(migrar_convenios_existentes, migrations.RunPython.noop),
        migrations.RemoveField(model_name="paciente", name="convenio"),
        migrations.RenameField(model_name="paciente", old_name="convenio_registro", new_name="convenio"),
        migrations.AlterField(
            model_name="paciente",
            name="convenio",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="pacientes", to="app.convenio", verbose_name="convênio"),
        ),
    ]
