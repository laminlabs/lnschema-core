# Generated by Django 4.2.1 on 2023-11-13 15:30

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_core", "0028_alter_dataset_visibility_alter_file_visibility"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="feature",
            name="modality",
        ),
        migrations.RemoveField(
            model_name="featureset",
            name="modality",
        ),
        migrations.DeleteModel(
            name="Modality",
        ),
    ]