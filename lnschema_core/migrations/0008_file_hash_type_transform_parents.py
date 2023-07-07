# Generated by Django 4.2.2 on 2023-07-07 11:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_core", "0007_feature_synonyms_featureset_field_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="file",
            name="hash_type",
            field=models.CharField(db_index=True, default=None, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name="transform",
            name="parents",
            field=models.ManyToManyField(related_name="children", to="lnschema_core.transform"),
        ),
    ]
