# Generated by Django 4.2.2 on 2023-06-16 15:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_core", "0002_alter_user_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="storage",
            name="region",
            field=models.CharField(db_index=True, default=None, max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name="transform",
            name="short_name",
            field=models.CharField(db_index=True, default=None, max_length=128, null=True),
        ),
    ]
