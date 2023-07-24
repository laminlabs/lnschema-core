# Generated by Django 4.2.2 on 2023-07-24 16:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_core", "0011_label_remove_tag_created_by_remove_tag_parents_and_more"),
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
            field=models.CharField(db_index=True, default=None, max_length=40, null=True),
        ),
        migrations.AddField(
            model_name="feature",
            name="labels_schema",
            field=models.CharField(db_index=True, default=None, max_length=40, null=True),
        ),
        migrations.CreateModel(
            name="FileFeatureSet",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("slot", models.CharField(default=None, max_length=40, null=True)),
                ("feature_set", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="lnschema_core.featureset")),
                ("file", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="lnschema_core.file")),
            ],
            options={
                "unique_together": {("file", "feature_set")},
            },
        ),
        migrations.CreateModel(
            name="DatasetFeatureSet",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("slot", models.CharField(default=None, max_length=50, null=True)),
                ("dataset", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="lnschema_core.dataset")),
                ("feature_set", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="lnschema_core.featureset")),
            ],
            options={
                "unique_together": {("dataset", "feature_set")},
            },
        ),
        migrations.RunSQL("CREATE TABLE lnschema_core_filefeatureset_tmp (id BIGINT, file_id TEXT, feature_set_id TEXT)"),
        migrations.RunSQL("INSERT INTO lnschema_core_filefeatureset_tmp (id, file_id, feature_set_id) SELECT id, file_id, featureset_id from lnschema_core_file_feature_sets"),
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
            field=models.ManyToManyField(related_name="datasets", through="lnschema_core.DatasetFeatureSet", to="lnschema_core.featureset"),
        ),
        migrations.AddField(
            model_name="file",
            name="feature_sets",
            field=models.ManyToManyField(related_name="files", through="lnschema_core.FileFeatureSet", to="lnschema_core.featureset"),
        ),
        migrations.RunSQL("INSERT INTO lnschema_core_filefeatureset (id, file_id, feature_set_id) SELECT id, file_id, feature_set_id from lnschema_core_filefeatureset_tmp"),
        migrations.RunSQL("DROP TABLE lnschema_core_filefeatureset_tmp"),
    ]
