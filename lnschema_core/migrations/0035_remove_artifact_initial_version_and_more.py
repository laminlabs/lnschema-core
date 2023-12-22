# Generated by Django 4.2.5 on 2023-12-22 23:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_core", "0034_run_environment"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="artifact",
            name="initial_version",
        ),
        migrations.RemoveField(
            model_name="dataset",
            name="initial_version",
        ),
        migrations.RemoveField(
            model_name="transform",
            name="initial_version",
        ),
        migrations.AlterField(
            model_name="transform",
            name="uid",
            field=models.CharField(db_index=True, default=None, max_length=16, unique=True),
        ),
    ]
