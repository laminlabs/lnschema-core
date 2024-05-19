# Generated by Django 5.0.6 on 2024-05-19 09:13

import django.db.models.deletion
from django.db import migrations, models

import lnschema_core.models
import lnschema_core.users


class Migration(migrations.Migration):
    dependencies = [
        (
            "lnschema_core",
            "0051_remove_feature_feature_sets_featuresetfeature_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="featureset",
            name="updated_at",
        ),
        migrations.RemoveField(
            model_name="run",
            name="json",
        ),
        migrations.RemoveField(
            model_name="run",
            name="replicated_output_artifacts",
        ),
        migrations.RemoveField(
            model_name="run",
            name="replicated_output_collections",
        ),
        migrations.AddField(
            model_name="artifact",
            name="previous_runs",
            field=models.ManyToManyField(to="lnschema_core.run"),
        ),
        migrations.AddField(
            model_name="collection",
            name="previous_runs",
            field=models.ManyToManyField(to="lnschema_core.run"),
        ),
        migrations.AddField(
            model_name="feature",
            name="previous_runs",
            field=models.ManyToManyField(to="lnschema_core.run"),
        ),
        migrations.AddField(
            model_name="feature",
            name="run",
            field=models.ForeignKey(
                default=lnschema_core.models.current_run,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="lnschema_core.run",
            ),
        ),
        migrations.AddField(
            model_name="featureset",
            name="run",
            field=models.ForeignKey(
                default=lnschema_core.models.current_run,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="lnschema_core.run",
            ),
        ),
        migrations.AddField(
            model_name="featurevalue",
            name="run",
            field=models.ForeignKey(
                default=lnschema_core.models.current_run,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="lnschema_core.run",
            ),
        ),
        migrations.AddField(
            model_name="param",
            name="previous_runs",
            field=models.ManyToManyField(to="lnschema_core.run"),
        ),
        migrations.AddField(
            model_name="param",
            name="run",
            field=models.ForeignKey(
                default=lnschema_core.models.current_run,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="lnschema_core.run",
            ),
        ),
        migrations.AddField(
            model_name="paramvalue",
            name="run",
            field=models.ForeignKey(
                default=lnschema_core.models.current_run,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="lnschema_core.run",
            ),
        ),
        migrations.AddField(
            model_name="storage",
            name="previous_runs",
            field=models.ManyToManyField(to="lnschema_core.run"),
        ),
        migrations.AddField(
            model_name="storage",
            name="run",
            field=models.ForeignKey(
                default=lnschema_core.models.current_run,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="lnschema_core.run",
            ),
        ),
        migrations.AddField(
            model_name="ulabel",
            name="previous_runs",
            field=models.ManyToManyField(to="lnschema_core.run"),
        ),
        migrations.AddField(
            model_name="ulabel",
            name="run",
            field=models.ForeignKey(
                default=lnschema_core.models.current_run,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="lnschema_core.run",
            ),
        ),
        migrations.AlterField(
            model_name="artifact",
            name="created_by",
            field=models.ForeignKey(
                default=lnschema_core.users.current_user_id,
                on_delete=django.db.models.deletion.PROTECT,
                to="lnschema_core.user",
            ),
        ),
        migrations.AlterField(
            model_name="collection",
            name="created_by",
            field=models.ForeignKey(
                default=lnschema_core.users.current_user_id,
                on_delete=django.db.models.deletion.PROTECT,
                to="lnschema_core.user",
            ),
        ),
        migrations.AlterField(
            model_name="feature",
            name="created_by",
            field=models.ForeignKey(
                default=lnschema_core.users.current_user_id,
                on_delete=django.db.models.deletion.PROTECT,
                to="lnschema_core.user",
            ),
        ),
        migrations.AlterField(
            model_name="featureset",
            name="created_by",
            field=models.ForeignKey(
                default=lnschema_core.users.current_user_id,
                on_delete=django.db.models.deletion.PROTECT,
                to="lnschema_core.user",
            ),
        ),
        migrations.AlterField(
            model_name="featurevalue",
            name="created_by",
            field=models.ForeignKey(
                default=lnschema_core.users.current_user_id,
                on_delete=django.db.models.deletion.PROTECT,
                to="lnschema_core.user",
            ),
        ),
        migrations.AlterField(
            model_name="param",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name="param",
            name="created_by",
            field=models.ForeignKey(
                default=lnschema_core.users.current_user_id,
                on_delete=django.db.models.deletion.PROTECT,
                to="lnschema_core.user",
            ),
        ),
        migrations.AlterField(
            model_name="paramvalue",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name="paramvalue",
            name="created_by",
            field=models.ForeignKey(
                default=lnschema_core.users.current_user_id,
                on_delete=django.db.models.deletion.PROTECT,
                to="lnschema_core.user",
            ),
        ),
        migrations.AlterField(
            model_name="storage",
            name="created_by",
            field=models.ForeignKey(
                default=lnschema_core.users.current_user_id,
                on_delete=django.db.models.deletion.PROTECT,
                to="lnschema_core.user",
            ),
        ),
        migrations.AlterField(
            model_name="ulabel",
            name="created_by",
            field=models.ForeignKey(
                default=lnschema_core.users.current_user_id,
                on_delete=django.db.models.deletion.PROTECT,
                to="lnschema_core.user",
            ),
        ),
    ]
