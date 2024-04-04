# Generated by Django 4.2.2 on 2023-07-24 09:35

import django.db.models.deletion
from django.db import migrations, models

import lnschema_core.ids
import lnschema_core.users


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_core", "0010_dataset_categories_file_categories"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Tag",
            new_name="Label",
        ),
        migrations.RenameField(
            model_name="featureset",
            old_name="field",
            new_name="ref_field",
        ),
        migrations.RenameField(
            model_name="featureset",
            old_name="schema",
            new_name="ref_schema",
        ),
        migrations.RenameField(
            model_name="file",
            old_name="tags",
            new_name="labels",
        ),
        migrations.RemoveField(
            model_name="dataset",
            name="categories",
        ),
        migrations.RemoveField(
            model_name="file",
            name="categories",
        ),
        migrations.AddField(
            model_name="dataset",
            name="labels",
            field=models.ManyToManyField(
                related_name="datasets", to="lnschema_core.label"
            ),
        ),
        migrations.AddField(
            model_name="featureset",
            name="n",
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="featureset",
            name="name",
            field=models.CharField(default=None, max_length=128, null=True),
        ),
        migrations.AddField(
            model_name="featureset",
            name="readout",
            field=models.CharField(default=None, max_length=64, null=True),
        ),
        migrations.AddField(
            model_name="featureset",
            name="ref_orm",
            field=models.CharField(db_index=True, default="Feature", max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="label",
            name="feature",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="labels",
                to="lnschema_core.feature",
            ),
        ),
        migrations.AddField(
            model_name="label",
            name="ref_id",
            field=models.CharField(default=None, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="label",
            name="ref_orm",
            field=models.CharField(default=None, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="label",
            name="ref_schema",
            field=models.CharField(default=None, max_length=30, null=True),
        ),
        migrations.RunSQL(
            "UPDATE lnschema_core_feature SET type='float' where type IS NULL"
        ),
        migrations.AlterField(
            model_name="feature",
            name="type",
            field=models.CharField(db_index=True, default=None, max_length=64),
        ),
        migrations.AlterField(
            model_name="featureset",
            name="type",
            field=models.CharField(default=None, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name="file",
            name="run",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="output_files",
                to="lnschema_core.run",
            ),
        ),
        migrations.AlterField(
            model_name="file",
            name="transform",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="files",
                to="lnschema_core.transform",
            ),
        ),
        migrations.AlterField(
            model_name="label",
            name="created_by",
            field=models.ForeignKey(
                default=lnschema_core.users.current_user_id,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="created_labels",
                to="lnschema_core.user",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="label",
            unique_together={("name", "feature")},
        ),
        migrations.DeleteModel(
            name="Category",
        ),
    ]
