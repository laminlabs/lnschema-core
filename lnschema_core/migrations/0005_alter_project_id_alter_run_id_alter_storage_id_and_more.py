# Generated by Django 4.2.1 on 2023-06-02 07:25

from django.db import migrations, models

import lnschema_core.dev._id


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_core", "0004_alter_folder_created_at_alter_folder_updated_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="id",
            field=models.CharField(default=lnschema_core.dev._id.project, max_length=8, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="run",
            name="id",
            field=models.CharField(default=lnschema_core.dev._id.run, max_length=12, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="storage",
            name="id",
            field=models.CharField(default=lnschema_core.dev._id.storage, max_length=8, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="transform",
            name="id",
            field=models.CharField(default=lnschema_core.dev._id.transform, max_length=12, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="user",
            name="id",
            field=models.CharField(max_length=8, primary_key=True, serialize=False),
        ),
    ]
