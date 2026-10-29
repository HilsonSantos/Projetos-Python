from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("app", "0006_usuario")]

    operations = [
        migrations.RunSQL(
            """
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM pg_constraint
                    WHERE conname = 'app_empresa_usuario_id_app_usuario_id_fk'
                ) THEN
                    ALTER TABLE app_empresa
                        ADD CONSTRAINT app_empresa_usuario_id_app_usuario_id_fk
                        FOREIGN KEY (usuario_id) REFERENCES app_usuario (id)
                        DEFERRABLE INITIALLY DEFERRED;
                END IF;
            END $$;
            """,
            migrations.RunSQL.noop,
        ),
    ]
