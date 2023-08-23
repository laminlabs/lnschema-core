# Generated by Django 4.2.2 on 2023-08-22 16:43

import django.db.models.deletion
from django.db import migrations, models

import lnschema_core.models


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_core", "0015_file_initial_version_file_version"),
    ]

    operations = [
        migrations.AddField(
            model_name="dataset",
            name="input_of",
            field=models.ManyToManyField(related_name="input_datasets", to="lnschema_core.run"),
        ),
        migrations.AddField(
            model_name="dataset",
            name="run",
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="output_datasets", to="lnschema_core.run"),
        ),
        migrations.AddField(
            model_name="dataset",
            name="transform",
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="datasets", to="lnschema_core.transform"),
        ),
        migrations.CreateModel(
            name="DatasetLabel",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("dataset", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="lnschema_core.dataset")),
                ("feature", models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to="lnschema_core.feature")),
                ("label", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="lnschema_core.label")),
            ],
            options={
                "unique_together": {("dataset", "label")},
            },
            bases=(models.Model, lnschema_core.models.LinkORM),
        ),
        migrations.RemoveField(
            model_name="dataset",
            name="labels",
        ),
        migrations.AddField(
            model_name="dataset",
            name="labels",
            field=models.ManyToManyField(related_name="datasets", through="lnschema_core.DatasetLabel", to="lnschema_core.label"),
        ),
        migrations.AddField(
            model_name="feature",
            name="modality",
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="features", to="lnschema_core.modality"),
        ),
        migrations.AlterField(
            model_name="featureset",
            name="modality",
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="feature_sets", to="lnschema_core.modality"),
        ),
        migrations.AlterUniqueTogether(
            name="transform",
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name="transform",
            name="stem_id",
        ),
        migrations.AddField(
            model_name="transform",
            name="initial_version",
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to="lnschema_core.transform"),
        ),
        migrations.AlterField(
            model_name="transform",
            name="version",
            field=models.CharField(db_index=True, default=None, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="storage",
            name="root",
            field=models.CharField(db_index=True, default=None, max_length=255, unique=True),
        ),
        migrations.RunSQL("UPDATE lnschema_core_file SET suffix = '' WHERE suffix IS NULL"),
        migrations.AlterField(
            model_name="file",
            name="suffix",
            field=models.CharField(db_index=True, default=None, max_length=30),
        ),
    ]
