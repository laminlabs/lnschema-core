# Generated by Django 4.2.1 on 2023-06-02 09:09

import django.db.models.deletion
from django.db import migrations, models

import lnschema_core._users
import lnschema_core.dev._id


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_core", "0005_alter_project_id_alter_run_id_alter_storage_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="transform",
            name="hash",
            field=models.CharField(default=lnschema_core.dev._id.transform, max_length=12),
        ),
        migrations.AlterField(
            model_name="features",
            name="created_by",
            field=models.ForeignKey(default=lnschema_core._users.current_user_id, on_delete=django.db.models.deletion.DO_NOTHING, to="lnschema_core.user"),
        ),
        migrations.AlterField(
            model_name="file",
            name="created_by",
            field=models.ForeignKey(default=lnschema_core._users.current_user_id, on_delete=django.db.models.deletion.DO_NOTHING, to="lnschema_core.user"),
        ),
        migrations.AlterField(
            model_name="folder",
            name="created_by",
            field=models.ForeignKey(default=lnschema_core._users.current_user_id, on_delete=django.db.models.deletion.DO_NOTHING, to="lnschema_core.user"),
        ),
        migrations.AlterField(
            model_name="project",
            name="created_by",
            field=models.ForeignKey(default=lnschema_core._users.current_user_id, on_delete=django.db.models.deletion.DO_NOTHING, to="lnschema_core.user"),
        ),
        migrations.AlterField(
            model_name="run",
            name="created_by",
            field=models.ForeignKey(default=lnschema_core._users.current_user_id, on_delete=django.db.models.deletion.DO_NOTHING, to="lnschema_core.user"),
        ),
        migrations.AlterField(
            model_name="storage",
            name="created_by",
            field=models.ForeignKey(
                blank=True, default=lnschema_core._users.current_user_id, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to="lnschema_core.user"
            ),
        ),
        migrations.AlterField(
            model_name="transform",
            name="created_by",
            field=models.ForeignKey(default=lnschema_core._users.current_user_id, on_delete=django.db.models.deletion.DO_NOTHING, to="lnschema_core.user"),
        ),
        migrations.AlterField(
            model_name="transform",
            name="id",
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID"),
        ),
        migrations.AlterField(
            model_name="transform",
            name="version",
            field=models.CharField(default="0", max_length=10),
        ),
    ]
