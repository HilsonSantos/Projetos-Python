from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [("app", "0016_usuario_profissao")]

    operations = [
        migrations.CreateModel(
            name="Paciente",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome_completo", models.CharField(max_length=200, verbose_name="nome completo")),
                ("cpf", models.CharField(max_length=14, verbose_name="CPF")),
                ("data_nascimento", models.DateField(verbose_name="data de nascimento")),
                ("sexo", models.CharField(blank=True, choices=[("F", "Feminino"), ("M", "Masculino"), ("O", "Outro"), ("N", "Prefiro não informar")], max_length=1, verbose_name="sexo")),
                ("telefone", models.CharField(max_length=20, verbose_name="telefone")),
                ("whatsapp", models.CharField(blank=True, max_length=20, verbose_name="WhatsApp")),
                ("email", models.EmailField(blank=True, max_length=254, verbose_name="e-mail")),
                ("cep", models.CharField(max_length=9, verbose_name="CEP")),
                ("logradouro", models.CharField(max_length=150, verbose_name="logradouro")),
                ("numero", models.CharField(max_length=20, verbose_name="número")),
                ("complemento", models.CharField(blank=True, max_length=100, verbose_name="complemento")),
                ("bairro", models.CharField(max_length=100, verbose_name="bairro")),
                ("cidade", models.CharField(max_length=100, verbose_name="cidade")),
                ("estado", models.CharField(max_length=2, verbose_name="UF")),
                ("contato_emergencia_nome", models.CharField(blank=True, max_length=150, verbose_name="nome do contato de emergência")),
                ("contato_emergencia_telefone", models.CharField(blank=True, max_length=20, verbose_name="telefone de emergência")),
                ("convenio", models.CharField(blank=True, max_length=120, verbose_name="convênio")),
                ("numero_carteirinha", models.CharField(blank=True, max_length=50, verbose_name="número da carteirinha")),
                ("observacoes", models.TextField(blank=True, verbose_name="observações")),
                ("criado_em", models.DateTimeField(auto_now_add=True)),
                ("atualizado_em", models.DateTimeField(auto_now=True)),
                ("empresa", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="pacientes", to="app.empresa")),
            ],
            options={
                "verbose_name": "paciente",
                "verbose_name_plural": "pacientes",
                "db_table": "pacientes",
                "ordering": ["nome_completo"],
                "constraints": [models.UniqueConstraint(fields=("empresa", "cpf"), name="uniq_paciente_cpf_empresa")],
            },
        ),
    ]
