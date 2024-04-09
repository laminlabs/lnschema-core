# Generated by Django 4.2.2 on 2023-07-24 16:50

import django.db.models.deletion
from django.db import migrations, models

import lnschema_core.ids


class Migration(migrations.Migration):
    dependencies = [
        (
            "lnschema_core",
            "0011_label_remove_tag_created_by_remove_tag_parents_and_more",
        ),
    ]

    operations = [
        migrations.RemoveField(
            model_name="label",
            name="ref_id",
        ),
        migrations.RemoveField(
            model_name="label",
            name="ref_orm",
        ),
        migrations.RemoveField(
            model_name="label",
            name="ref_schema",
        ),
        migrations.AddField(
            model_name="feature",
            name="labels_orm",
            field=models.CharField(
                db_index=True, default=None, max_length=40, null=True
            ),
        ),
        migrations.AddField(
            model_name="feature",
            name="labels_schema",
            field=models.CharField(
                db_index=True, default=None, max_length=40, null=True
            ),
        ),
        migrations.CreateModel(
            name="FileFeatureSet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("slot", models.CharField(default=None, max_length=40, null=True)),
                (
                    "feature_set",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="lnschema_core.featureset",
                    ),
                ),
                (
                    "file",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="lnschema_core.file",
                    ),
                ),
            ],
            options={
                "unique_together": {("file", "feature_set")},
            },
        ),
        migrations.CreateModel(
            name="DatasetFeatureSet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("slot", models.CharField(default=None, max_length=50, null=True)),
                (
                    "dataset",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="lnschema_core.dataset",
                    ),
                ),
                (
                    "feature_set",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="lnschema_core.featureset",
                    ),
                ),
            ],
            options={
                "unique_together": {("dataset", "feature_set")},
            },
        ),
        migrations.RunSQL(
            "CREATE TABLE lnschema_core_filefeatureset_tmp (id BIGINT, file_id TEXT, feature_set_id TEXT)"
        ),
        migrations.RunSQL(
            "INSERT INTO lnschema_core_filefeatureset_tmp (id, file_id, feature_set_id) SELECT id, file_id, featureset_id from lnschema_core_file_feature_sets"
        ),
        migrations.RemoveField(
            model_name="file",
            name="feature_sets",
        ),
        migrations.RemoveField(
            model_name="dataset",
            name="feature_sets",
        ),
        migrations.AddField(
            model_name="dataset",
            name="feature_sets",
            field=models.ManyToManyField(
                related_name="datasets",
                through="lnschema_core.DatasetFeatureSet",
                to="lnschema_core.featureset",
            ),
        ),
        migrations.AddField(
            model_name="file",
            name="feature_sets",
            field=models.ManyToManyField(
                related_name="files",
                through="lnschema_core.FileFeatureSet",
                to="lnschema_core.featureset",
            ),
        ),
        migrations.RunSQL(
            "INSERT INTO lnschema_core_filefeatureset (id, file_id, feature_set_id) SELECT id, file_id, feature_set_id from lnschema_core_filefeatureset_tmp"
        ),
        migrations.RunSQL("DROP TABLE lnschema_core_filefeatureset_tmp"),
        migrations.AddField(
            model_name="file",
            name="accessor",
            field=models.CharField(
                db_index=True, default=None, max_length=64, null=True
            ),
        ),
        migrations.RemoveField(
            model_name="featureset",
            name="readout",
        ),
        migrations.CreateModel(
            name="Modality",
            fields=[
                (
                    "id",
                    models.CharField(
                        default=lnschema_core.ids.base62_8,
                        max_length=8,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=256)),
                (
                    "ontology_id",
                    models.CharField(
                        db_index=True, default=None, max_length=32, null=True
                    ),
                ),
                (
                    "abbr",
                    models.CharField(
                        db_index=True,
                        default=None,
                        max_length=32,
                        null=True,
                        unique=True,
                    ),
                ),
                ("synonyms", models.TextField(default=None, null=True)),
                ("description", models.TextField(default=None, null=True)),
                ("molecule", models.TextField(db_index=True, default=None, null=True)),
                (
                    "instrument",
                    models.TextField(db_index=True, default=None, null=True),
                ),
                (
                    "measurement",
                    models.TextField(db_index=True, default=None, null=True),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        default=lnschema_core.users.current_user_id,
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="created_modalities",
                        to="lnschema_core.user",
                    ),
                ),
                (
                    "parents",
                    models.ManyToManyField(
                        related_name="children", to="lnschema_core.modality"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="featureset",
            name="modality",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="lnschema_core.modality",
            ),
        ),
        migrations.AlterField(
            model_name="featureset",
            name="created_by",
            field=models.ForeignKey(
                default=lnschema_core.users.current_user_id,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="created_feature_sets",
                to="lnschema_core.user",
            ),
        ),
        migrations.AddField(
            model_name="featureset",
            name="hash",
            field=models.CharField(
                db_index=True, default=None, max_length=20, null=True
            ),
        ),
    ]
