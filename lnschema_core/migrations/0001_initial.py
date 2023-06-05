# Generated by Django 4.2.1 on 2023-06-04 13:33

from typing import List

import django.db.models.deletion
from django.db import migrations, models

import lnschema_core._types
import lnschema_core._users
import lnschema_core.ids


class Migration(migrations.Migration):
    initial = True

    dependencies: List[str] = []

    operations = [
        migrations.CreateModel(
            name="File",
            fields=[
                ("id", models.CharField(max_length=20, primary_key=True, serialize=False)),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                ("suffix", models.CharField(blank=True, max_length=63, null=True)),
                ("size", models.BigIntegerField(blank=True, null=True)),
                ("hash", models.CharField(blank=True, max_length=63, null=True)),
                ("key", models.CharField(blank=True, max_length=255, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="Folder",
            fields=[
                ("id", models.CharField(max_length=20, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("key", models.CharField(blank=True, max_length=255, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="Run",
            fields=[
                ("id", models.CharField(default=lnschema_core.ids.run, max_length=12, primary_key=True, serialize=False)),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                ("external_id", models.CharField(blank=True, max_length=255, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.CharField(max_length=8, primary_key=True, serialize=False)),
                ("email", models.CharField(max_length=64, unique=True)),
                ("handle", models.CharField(max_length=64, unique=True)),
                ("name", models.CharField(blank=True, max_length=64, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="Transform",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("hash", models.CharField(default=lnschema_core.ids.transform, max_length=12)),
                ("version", models.CharField(default="0", max_length=10)),
                (
                    "type",
                    models.CharField(
                        choices=[("pipeline", "pipeline"), ("notebook", "notebook"), ("app", "app")],
                        db_index=True,
                        default=lnschema_core._types.TransformType["pipeline"],
                        max_length=63,
                    ),
                ),
                ("title", models.TextField(blank=True, null=True)),
                ("reference", models.CharField(blank=True, max_length=255, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_by", models.ForeignKey(default=lnschema_core._users.current_user_id, on_delete=django.db.models.deletion.DO_NOTHING, to="lnschema_core.user")),
            ],
            options={
                "managed": True,
                "unique_together": {("name", "version")},
            },
        ),
        migrations.CreateModel(
            name="Storage",
            fields=[
                ("id", models.CharField(default=lnschema_core.ids.storage, max_length=8, primary_key=True, serialize=False)),
                ("root", models.CharField(max_length=255)),
                ("type", models.CharField(blank=True, max_length=63, null=True)),
                ("region", models.CharField(blank=True, max_length=63, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True, default=lnschema_core._users.current_user_id, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to="lnschema_core.user"
                    ),
                ),
            ],
            options={
                "managed": True,
            },
        ),
        migrations.CreateModel(
            name="RunInput",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("file", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="lnschema_core.file")),
                ("run", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="lnschema_core.run")),
            ],
            options={
                "managed": True,
            },
        ),
        migrations.AddField(
            model_name="run",
            name="created_by",
            field=models.ForeignKey(default=lnschema_core._users.current_user_id, on_delete=django.db.models.deletion.DO_NOTHING, to="lnschema_core.user"),
        ),
        migrations.AddField(
            model_name="run",
            name="inputs",
            field=models.ManyToManyField(related_name="input_of", through="lnschema_core.RunInput", to="lnschema_core.file"),
        ),
        migrations.AddField(
            model_name="run",
            name="transform",
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to="lnschema_core.transform"),
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                ("id", models.CharField(default=lnschema_core.ids.project, max_length=8, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=64)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("created_by", models.ForeignKey(default=lnschema_core._users.current_user_id, on_delete=django.db.models.deletion.DO_NOTHING, to="lnschema_core.user")),
                ("files", models.ManyToManyField(to="lnschema_core.file")),
                ("folders", models.ManyToManyField(to="lnschema_core.folder")),
            ],
            options={
                "managed": True,
            },
        ),
        migrations.AddField(
            model_name="folder",
            name="created_by",
            field=models.ForeignKey(default=lnschema_core._users.current_user_id, on_delete=django.db.models.deletion.DO_NOTHING, to="lnschema_core.user"),
        ),
        migrations.AddField(
            model_name="folder",
            name="files",
            field=models.ManyToManyField(to="lnschema_core.file"),
        ),
        migrations.AddField(
            model_name="folder",
            name="storage",
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to="lnschema_core.storage"),
        ),
        migrations.AddField(
            model_name="file",
            name="created_by",
            field=models.ForeignKey(default=lnschema_core._users.current_user_id, on_delete=django.db.models.deletion.DO_NOTHING, to="lnschema_core.user"),
        ),
        migrations.AddField(
            model_name="file",
            name="run",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name="outputs", to="lnschema_core.run"),
        ),
        migrations.AddField(
            model_name="file",
            name="storage",
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to="lnschema_core.storage"),
        ),
        migrations.AddField(
            model_name="file",
            name="transform",
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to="lnschema_core.transform"),
        ),
        migrations.CreateModel(
            name="Featureset",
            fields=[
                ("id", models.CharField(max_length=63, primary_key=True, serialize=False)),
                ("type", models.CharField(max_length=63)),
                ("created_at", models.DateTimeField(auto_now=True)),
                ("created_by", models.ForeignKey(default=lnschema_core._users.current_user_id, on_delete=django.db.models.deletion.DO_NOTHING, to="lnschema_core.user")),
                ("files", models.ManyToManyField(to="lnschema_core.file")),
            ],
            options={
                "managed": True,
            },
        ),
        migrations.AlterUniqueTogether(
            name="folder",
            unique_together={("storage", "key")},
        ),
        migrations.AlterUniqueTogether(
            name="file",
            unique_together={("storage", "key")},
        ),
    ]
