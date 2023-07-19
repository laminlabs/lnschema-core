# Generated by Django 4.2.2 on 2023-07-19 11:34

import django.db.models.deletion
from django.db import migrations, models

import lnschema_core.users


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_core", "0008_file_hash_type_transform_parents"),
    ]

    operations = [
        migrations.AddField(
            model_name="feature",
            name="field",
            field=models.CharField(default=None, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="feature",
            name="unit",
            field=models.CharField(default=None, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name="featureset",
            name="field",
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name="run",
            name="created_by",
            field=models.ForeignKey(
                default=lnschema_core.users.current_user_id, on_delete=django.db.models.deletion.CASCADE, related_name="created_runs", to="lnschema_core.user"
            ),
        ),
        migrations.AlterField(
            model_name="run",
            name="transform",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="runs", to="lnschema_core.transform"),
        ),
        migrations.CreateModel(
            name="FeatureValue",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("value", models.CharField(max_length=128)),
                ("feature", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="values", to="lnschema_core.feature")),
            ],
            options={
                "unique_together": {("feature", "value")},
            },
        ),
        migrations.RemoveField(
            model_name="featureset",
            name="files",
        ),
        migrations.AddField(
            model_name="file",
            name="feature_sets",
            field=models.ManyToManyField(related_name="files", to="lnschema_core.featureset"),
        ),
    ]
