# Generated by Django 4.2.1 on 2023-09-15 08:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_core", "0018_rename_datasetlabel_datasetulabel_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="dataset",
            name="reference",
            field=models.CharField(db_index=True, default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="dataset",
            name="reference_type",
            field=models.CharField(db_index=True, default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="transform",
            name="reference_type",
            field=models.CharField(db_index=True, default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="ulabel",
            name="reference",
            field=models.CharField(db_index=True, default=None, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="ulabel",
            name="reference_type",
            field=models.CharField(db_index=True, default=None, max_length=255, null=True),
        ),
    ]