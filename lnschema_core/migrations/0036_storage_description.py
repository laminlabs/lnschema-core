# Generated by Django 4.2.5 on 2023-12-23 22:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_core", "0035_remove_artifact_initial_version_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="storage",
            name="description",
            field=models.CharField(db_index=True, default=None, max_length=255),
        ),
    ]