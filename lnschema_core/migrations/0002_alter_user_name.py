# Generated by Django 4.2.2 on 2023-06-15 02:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="name",
            field=models.CharField(
                db_index=True, default=None, max_length=255, null=True
            ),
        ),
    ]
