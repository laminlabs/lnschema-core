# Generated by Django 4.2.2 on 2023-08-10 11:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_core", "0014_rename_ref_field_featureset_registry"),
    ]

    operations = [
        migrations.AddField(
            model_name="file",
            name="initial_version",
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to="lnschema_core.file"),
        ),
        migrations.AddField(
            model_name="file",
            name="version",
            field=models.CharField(db_index=True, default=None, max_length=10, null=True),
        ),
    ]
