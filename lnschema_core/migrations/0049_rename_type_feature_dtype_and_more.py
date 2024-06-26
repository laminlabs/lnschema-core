# Generated by Django 5.0.6 on 2024-05-17 20:14

from django.db import connection, migrations


def reset_pending_trigger_events(apps, schema_editor):
    if connection.vendor != "sqlite":
        with schema_editor.connection.cursor() as cursor:
            cursor.execute("SET CONSTRAINTS ALL IMMEDIATE;")


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_core", "0048_alter_artifactulabel_feature_and_more"),
    ]

    operations = [
        migrations.RunPython(reset_pending_trigger_events),
        migrations.RenameField(
            model_name="feature",
            old_name="type",
            new_name="dtype",
        ),
        migrations.RunSQL(
            """
            -- Update "dtype" where the old value was "category"
            UPDATE lnschema_core_feature
            SET dtype = CASE
                WHEN registries IS NOT NULL THEN 'cat[' || registries || ']'
                ELSE 'cat'
            END
            WHERE dtype = 'category';
            """
        ),
        migrations.RunSQL(
            """
            -- Replace all occurrences of "core." in dtype with an empty string
            UPDATE lnschema_core_feature
            SET dtype = REPLACE(dtype, 'core.', '');
            """
        ),
        migrations.RenameField(
            model_name="featureset",
            old_name="type",
            new_name="dtype",
        ),
        migrations.RunSQL(
            """
            -- Replace all occurrences of "core." in dtype with an empty string
            UPDATE lnschema_core_featureset
            SET registry = REPLACE(registry, 'core.', '');
            """
        ),
        migrations.RemoveField(
            model_name="feature",
            name="registries",
        ),
    ]
