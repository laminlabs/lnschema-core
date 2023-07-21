# Generated by Django 4.2.2 on 2023-07-21 07:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_core", "0009_remove_featureset_files_feature_unit_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="dataset",
            name="categories",
            field=models.ManyToManyField(related_name="datasets", to="lnschema_core.category"),
        ),
        migrations.AddField(
            model_name="file",
            name="categories",
            field=models.ManyToManyField(related_name="files", to="lnschema_core.category"),
        ),
        migrations.AddField(
            model_name="tag",
            name="description",
            field=models.TextField(default=None, null=True),
        ),
        migrations.AddField(
            model_name="tag",
            name="parents",
            field=models.ManyToManyField(related_name="children", to="lnschema_core.tag"),
        ),
        migrations.RenameField(
            model_name="run",
            old_name="external_id",
            new_name="reference",
        ),
        migrations.RenameField(
            model_name="run",
            old_name="name",
            new_name="reference_type",
        ),
        migrations.DeleteModel(
            name="Project",
        ),
    ]
