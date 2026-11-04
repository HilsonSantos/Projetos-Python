from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("app", "0015_usuario_whatsapp")]

    operations = [
        migrations.AddField(
            model_name="usuario",
            name="profissao",
            field=models.CharField(
                blank=True,
                choices=[
                    ("MED", "Médico(a)"),
                    ("REC", "Recepcionista"),
                    ("ENF", "Enfermeiro(a)"),
                    ("TENF", "Técnico(a) de enfermagem"),
                    ("PSI", "Psicólogo(a)"),
                    ("FIS", "Fisioterapeuta"),
                    ("DEN", "Dentista"),
                    ("NUT", "Nutricionista"),
                    ("FAR", "Farmacêutico(a)"),
                    ("OUT", "Outro"),
                ],
                max_length=10,
                verbose_name="tipo de profissional",
            ),
        ),
    ]
