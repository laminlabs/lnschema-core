# Generated by Django 4.2.5 on 2023-10-08 03:00

import django.db.models.deletion
from django.db import connection, migrations, models

import lnschema_core.ids  # noqa
import lnschema_core.models

CORE_MODELS = {
    "Dataset": False,
    "File": False,
    "Transform": False,
    "Run": True,
    "User": False,
    "Storage": False,
    "Feature": False,
    "FeatureSet": False,
    "Modality": False,
    "ULabel": False,
}


def create_new_ids(apps, schema_editor):
    response = input(
        "\nDo you want to migrate your instance to integer primary keys? You will need"
        " to re-initialize your instance with `lamin init` after a data export. This is"
        " more cumbersome than a regular migration. (y/n)"
    )
    if response != "y":
        raise SystemExit
    for model_name in CORE_MODELS.keys():
        model_class = apps.get_model("lnschema_core", model_name)
        new_id = 1
        for record in model_class.objects.all().iterator(chunk_size=50):
            record.id = new_id
            record.save()
            new_id += 1


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_core", "0021_dataset_storage_alter_dataset_file"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dataset",
            name="transform",
            field=models.ForeignKey(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="output_datasets",
                to="lnschema_core.transform",
            ),
        ),
    ]


# repurpose old primary key
for model_name in CORE_MODELS.keys():
    Migration.operations.append(
        migrations.RenameField(
            model_name=model_name,
            old_name="id",
            new_name="uid",
        )
    )


# add new primary key field
for model_name, big in CORE_MODELS.items():
    Migration.operations.append(
        migrations.AddField(
            model_name=model_name,
            name="id",
            field=(models.BigIntegerField(editable=False, null=True) if big else models.IntegerField(editable=False, null=True)),
            preserve_default=False,
        )
    )

# fill in new id values in entity tables
Migration.operations.append(migrations.RunPython(create_new_ids, reverse_code=migrations.RunPython.noop))

# make them unique
for model_name, big in CORE_MODELS.items():
    Migration.operations.append(
        migrations.AlterField(
            model_name=model_name,
            name="id",
            field=(models.BigIntegerField(editable=False, unique=True) if big else models.IntegerField(editable=False, unique=True)),
            preserve_default=False,
        )
    )


def add_new_column_foreign_keys(apps, schema_editor):
    def add_new_column_foreign_keys_orm(orm):
        foreign_key_names = [field.name for field in orm._meta.fields if isinstance(field, (models.ForeignKey, models.OneToOneField))]
        for foreign_key_name in foreign_key_names:
            command1 = f"ALTER TABLE {orm._meta.db_table} RENAME COLUMN {foreign_key_name}_id TO {foreign_key_name}_id_old"
            command2 = f"ALTER TABLE {orm._meta.db_table} ADD {foreign_key_name}_id int"
            with connection.cursor() as cursor:
                cursor.execute(command1)
                cursor.execute(command2)
        many_to_many_names = [field.name for field in orm._meta.many_to_many]
        for many_to_many_name in many_to_many_names:
            link_orm = getattr(orm, many_to_many_name).through
            add_new_column_foreign_keys_orm(link_orm)

    for model_name in CORE_MODELS.keys():
        registry = getattr(lnschema_core.models, model_name)
        add_new_column_foreign_keys_orm(registry)


# add temporary ID fields
Migration.operations.append(migrations.RunPython(add_new_column_foreign_keys, reverse_code=migrations.RunPython.noop))


def populate_tmp_column_foreign_keys(orm):
    migrations_list = []
    foreign_key_names = [field.name for field in orm._meta.fields if isinstance(field, (models.ForeignKey, models.OneToOneField))]
    for foreign_key_name in foreign_key_names:
        related_table = orm._meta.get_field(foreign_key_name).related_model._meta.db_table
        table = orm._meta.db_table
        # need to use an alias below, otherwise self-referential foreign keys will be omitted
        command = f"UPDATE {table} SET {foreign_key_name}_id=(SELECT id FROM {related_table} b WHERE {table}.{foreign_key_name}_id_old=b.uid)"
        migrations_list.append(migrations.RunSQL(command))
    many_to_many_names = [field.name for field in orm._meta.many_to_many]
    for many_to_many_name in many_to_many_names:
        link_orm = getattr(orm, many_to_many_name).through
        migrations_list += populate_tmp_column_foreign_keys(link_orm)
    return migrations_list


# populate temporary fields
for model_name in CORE_MODELS.keys():
    try:
        registry = getattr(lnschema_core.models, model_name)
    except AttributeError:
        continue
    Migration.operations += populate_tmp_column_foreign_keys(registry)


# all what follows below is not running through for reasons that I (Alex) don't understand
# we'll keep it here to theoretically ascertain migration integrity

# turn previous primary keys into regular char fields
# Migration.operations += [
#     migrations.AlterField(
#         model_name="dataset",
#         name="uid",
#         field=models.CharField(db_index=True, default=lnschema_core.ids.base62_20, max_length=20, unique=True),
#     ),
#     migrations.AlterField(
#         model_name="datasetfeatureset",
#         name="id",
#         field=models.BigAutoField(primary_key=True, serialize=False),
#     ),
#     migrations.AlterField(
#         model_name="datasetulabel",
#         name="id",
#         field=models.BigAutoField(primary_key=True, serialize=False),
#     ),
#     migrations.AlterField(
#         model_name="feature",
#         name="uid",
#         field=models.CharField(db_index=True, default=lnschema_core.ids.base62_12, max_length=12, unique=True),
#     ),
#     migrations.AlterField(
#         model_name="featureset",
#         name="uid",
#         field=models.CharField(db_index=True, default=None, max_length=20, unique=True),
#     ),
#     migrations.AlterField(
#         model_name="file",
#         name="uid",
#         field=models.CharField(db_index=True, max_length=20, unique=True),
#     ),
#     migrations.AlterField(
#         model_name="filefeatureset",
#         name="id",
#         field=models.BigAutoField(primary_key=True, serialize=False),
#     ),
#     migrations.AlterField(
#         model_name="fileulabel",
#         name="id",
#         field=models.BigAutoField(primary_key=True, serialize=False),
#     ),
#     migrations.AlterField(
#         model_name="modality",
#         name="uid",
#         field=models.CharField(db_index=True, default=lnschema_core.ids.base62_8, max_length=8, unique=True),
#     ),
#     migrations.AlterField(
#         model_name="run",
#         name="uid",
#         field=models.CharField(db_index=True, default=lnschema_core.ids.base62_20, max_length=20, unique=True),
#     ),
#     migrations.AlterField(
#         model_name="storage",
#         name="uid",
#         field=models.CharField(db_index=True, default=lnschema_core.ids.base62_8, max_length=8, unique=True),
#     ),
#     migrations.AlterField(
#         model_name="transform",
#         name="uid",
#         field=models.CharField(db_index=True, default=None, max_length=14, unique=True),
#     ),
#     migrations.AlterField(
#         model_name="ulabel",
#         name="uid",
#         field=models.CharField(db_index=True, default=lnschema_core.ids.base62_8, max_length=8, unique=True),
#     ),
#     migrations.AlterField(
#         model_name="user",
#         name="uid",
#         field=models.CharField(db_index=True, default=None, max_length=8, unique=True),
#     ),
# ]


# # turn integer id fields into primary keys
# for model_name, big in CORE_MODELS.items():
#     Migration.operations.append(
#         migrations.AlterField(
#             model_name=model_name,
#             name="id",
#             field=models.BigAutoField(primary_key=True, serialize=False) if big else models.AutoField(primary_key=True, serialize=False),
#         ),
#     )


# # fix defaults for foreign keys and nullability
# Migration.operations += [
#     migrations.AlterField(
#         model_name="dataset",
#         name="created_by",
#         field=models.ForeignKey(
#             default=lnschema_core.users.current_user_id, on_delete=django.db.models.deletion.PROTECT, related_name="created_datasets", to="lnschema_core.user"
#         ),
#     ),
#     migrations.AlterField(
#         model_name="feature",
#         name="created_by",
#         field=models.ForeignKey(
#             default=lnschema_core.users.current_user_id, on_delete=django.db.models.deletion.PROTECT, related_name="created_features", to="lnschema_core.user"
#         ),
#     ),
#     migrations.AlterField(
#         model_name="featureset",
#         name="created_by",
#         field=models.ForeignKey(
#             default=lnschema_core.users.current_user_id, on_delete=django.db.models.deletion.PROTECT, related_name="created_feature_sets", to="lnschema_core.user"
#         ),
#     ),
#     migrations.AlterField(
#         model_name="file",
#         name="created_by",
#         field=models.ForeignKey(
#             default=lnschema_core.users.current_user_id, on_delete=django.db.models.deletion.PROTECT, related_name="created_files", to="lnschema_core.user"
#         ),
#     ),
#     migrations.AlterField(
#         model_name="file",
#         name="storage",
#         field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="files", to="lnschema_core.storage"),
#     ),
#     migrations.AlterField(
#         model_name="modality",
#         name="created_by",
#         field=models.ForeignKey(
#             default=lnschema_core.users.current_user_id, on_delete=django.db.models.deletion.PROTECT, related_name="created_modalities", to="lnschema_core.user"
#         ),
#     ),
#     migrations.AlterField(
#         model_name="run",
#         name="created_by",
#         field=models.ForeignKey(default=lnschema_core.users.current_user_id, on_delete=django.db.models.deletion.CASCADE, related_name="created_runs", to="lnschema_core.user"),  # noqa
#     ),
#     migrations.AlterField(
#         model_name="run",
#         name="transform",
#         field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="runs", to="lnschema_core.transform"),
#     ),
#     migrations.AlterField(
#         model_name="storage",
#         name="created_by",
#         field=models.ForeignKey(
#             default=lnschema_core.users.current_user_id, on_delete=django.db.models.deletion.PROTECT, related_name="created_storages", to="lnschema_core.user"
#         ),
#     ),
#     migrations.AlterField(
#         model_name="transform",
#         name="created_by",
#         field=models.ForeignKey(
#             default=lnschema_core.users.current_user_id, on_delete=django.db.models.deletion.PROTECT, related_name="created_transforms", to="lnschema_core.user"
#         ),
#     ),
#     migrations.AlterField(
#         model_name="ulabel",
#         name="created_by",
#         field=models.ForeignKey(
#             default=lnschema_core.users.current_user_id, on_delete=django.db.models.deletion.PROTECT, related_name="created_ulabels", to="lnschema_core.user"
#         ),
#     ),
# ]
