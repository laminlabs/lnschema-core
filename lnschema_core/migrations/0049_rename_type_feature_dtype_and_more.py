# Generated by Django 5.0.6 on 2024-05-17 20:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_core", "0048_alter_artifactulabel_feature_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="feature",
            old_name="type",
            new_name="dtype",
        ),
        migrations.RunSQL(
            """
            -- Update "dtype" where the old value was "category"
            UPDATE lnschema_core_feature
            SET dtype = 'cat[' || registries || ']'
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
        migrations.RemoveField(
            model_name="feature",
            name="registries",
        ),
    ]
