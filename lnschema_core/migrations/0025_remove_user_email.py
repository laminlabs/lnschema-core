# Generated by Django 4.2.5 on 2023-10-19 20:06

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_core", "0024_import_legacy_data"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="email",
        ),
    ]
