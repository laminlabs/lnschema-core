# Generated by Django 5.1 on 2024-06-13 10:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "lnschema_core",
            "0053_alter_featureset_hash_alter_paramvalue_created_by_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="feature",
            name="previous_runs",
            field=models.ManyToManyField(related_name="+", to="lnschema_core.run"),
        ),
        migrations.AlterField(
            model_name="param",
            name="previous_runs",
            field=models.ManyToManyField(related_name="+", to="lnschema_core.run"),
        ),
        migrations.AlterField(
            model_name="storage",
            name="previous_runs",
            field=models.ManyToManyField(related_name="+", to="lnschema_core.run"),
        ),
        migrations.AlterField(
            model_name="ulabel",
            name="previous_runs",
            field=models.ManyToManyField(related_name="+", to="lnschema_core.run"),
        ),
    ]
