# Generated by Django 4.2.2 on 2023-10-04 01:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_core", "0020_run_report_transform_latest_report_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="dataset",
            name="storage",
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name="datasets", to="lnschema_core.storage"),
        ),
        migrations.AlterField(
            model_name="dataset",
            name="file",
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name="dataset", to="lnschema_core.file"),
        ),
    ]