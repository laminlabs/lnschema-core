# Generated by Django 4.2.1 on 2023-11-23 20:27

from django.db import IntegrityError, migrations, models, transaction


def forwards_func(apps, schema_editor):
    File = apps.get_model("lnschema_core", "File")
    Dataset = apps.get_model("lnschema_core", "Dataset")
    db_alias = schema_editor.connection.alias
    # see https://stackoverflow.com/a/23326971
    try:
        with transaction.atomic():
            File.objects.using(db_alias).filter(visibility=0).update(visibility=1)
            File.objects.using(db_alias).filter(visibility=1).update(visibility=0)
            File.objects.using(db_alias).filter(visibility=2).update(visibility=-1)
            Dataset.objects.using(db_alias).filter(visibility=0).update(visibility=1)
            Dataset.objects.using(db_alias).filter(visibility=1).update(visibility=0)
            Dataset.objects.using(db_alias).filter(visibility=2).update(visibility=-1)
    except IntegrityError:
        pass


def reverse_func(apps, schema_editor):
    File = apps.get_model("lnschema_core", "File")
    Dataset = apps.get_model("lnschema_core", "Dataset")
    db_alias = schema_editor.connection.alias
    # see https://stackoverflow.com/a/23326971
    try:
        with transaction.atomic():
            File.objects.using(db_alias).filter(visibility=0).update(visibility=1)
            File.objects.using(db_alias).filter(visibility=1).update(visibility=0)
            File.objects.using(db_alias).filter(visibility=-1).update(visibility=2)
            Dataset.objects.using(db_alias).filter(visibility=0).update(visibility=1)
            Dataset.objects.using(db_alias).filter(visibility=1).update(visibility=0)
            Dataset.objects.using(db_alias).filter(visibility=-1).update(visibility=2)
    except IntegrityError:
        pass


class Migration(migrations.Migration):
    dependencies = [
        (
            "lnschema_core",
            "0029_remove_feature_modality_remove_featureset_modality_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="dataset",
            name="visibility",
            field=models.SmallIntegerField(
                choices=[(1, "Default"), (0, "Hidden"), (-1, "Trash")],
                db_index=True,
                default=0,
            ),
        ),
        migrations.AlterField(
            model_name="file",
            name="visibility",
            field=models.SmallIntegerField(
                choices=[(1, "Default"), (0, "Hidden"), (-1, "Trash")],
                db_index=True,
                default=0,
            ),
        ),
        migrations.RunPython(forwards_func, reverse_func),
    ]
