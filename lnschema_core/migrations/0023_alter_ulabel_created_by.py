import importlib
from typing import Dict, Union

import django.db.models.deletion
from django.db import migrations, models
from lamindb_setup import settings as _settings
from lamindb_setup._init_instance import get_schema_module_name

import lnschema_core.ids  # noqa
import lnschema_core.users
from lnschema_core.models import LinkORM


class SchemaMetadata:
    _models: Union[dict[str, dict[str, "ModelMetadata"]], None] = None

    @staticmethod
    def get_models():
        if SchemaMetadata._models is None:
            SchemaMetadata._models = get_models_metadata()
        return SchemaMetadata._models


class ModelMetadata:
    def __init__(self, model) -> None:
        self.model = model
        self.class_name = model.__name__
        self.model_name = model._meta.model_name
        self.relations = ModelRelations(model)
        self.fields_metadata = get_fields_metadata(self.model)


class ModelRelations:
    def __init__(self, model) -> None:
        self.many_to_one = {}
        self.one_to_many = {}
        self.many_to_many = {}
        self.one_to_one = {}

        for field in model._meta.get_fields():
            if field.many_to_one:
                self.many_to_one.update({field.name: field})
            elif field.one_to_many:
                self.one_to_many.update({field.name: field})
            elif field.many_to_many:
                self.many_to_many.update({field.name: field})
            elif field.one_to_one:
                self.one_to_one.update({field.name: field})

        self.all = {
            **self.many_to_one,
            **self.one_to_many,
            **self.many_to_many,
            **self.one_to_one,
        }


def get_fields_metadata(model):
    fields = {}

    for field in model._meta.fields:
        fields.update({field.name: get_field_metadata(model, field)})

    model_relations_metadata = ModelRelations(model)

    # One to many

    for relation_name, relation in model_relations_metadata.one_to_many.items():
        fields.update({f"{relation_name}": get_field_metadata(model, relation.field)})

    # Many to many

    for link_field_name, link_field in model_relations_metadata.many_to_many.items():
        fields.update({f"{link_field_name}": get_field_metadata(model, link_field)})

    # Many to one

    for link_field_name, link_field in model_relations_metadata.many_to_one.items():
        fields.update({f"{link_field_name}": get_field_metadata(model, link_field)})

    for link_field_name, link_field in model_relations_metadata.many_to_one.items():
        for field in link_field.related_model._meta.fields:
            fields.update({f"{link_field_name}__{field.name}": get_field_metadata(model, field)})

    # One to one

    for link_field_name, link_field in model_relations_metadata.one_to_one.items():
        fields.update({f"{link_field_name}": get_field_metadata(model, link_field)})

    for link_field_name, link_field in model_relations_metadata.one_to_one.items():
        for field in link_field.related_model._meta.fields:
            fields.update({f"{link_field_name}__{field.name}": get_field_metadata(model, field)})

    return fields


def get_field_metadata(model, field):
    internal_type = field.get_internal_type()
    model_name = field.model.__name__
    relation_type = get_relation_type(model, field)
    if field.related_model:
        related_model_name = field.related_model.__name__
        if relation_type == "one-to-many":
            related_schema_name = field.model._meta.app_label.replace("lnschema_", "")
            schema_name = field.related_model._meta.app_label.replace("lnschema_", "")
            related_field_name = field.name
            field_name = field.remote_field.name
        else:
            related_schema_name = field.related_model._meta.app_label.replace("lnschema_", "")
            schema_name = field.model._meta.app_label.replace("lnschema_", "")
            related_field_name = field.remote_field.name
            field_name = field.name
    else:
        schema_name = field.model._meta.app_label.replace("lnschema_", "")
        related_model_name = None
        related_schema_name = None
        related_field_name = None
        field_name = field.name

    if relation_type in ["one-to-many"]:
        model_name, related_model_name = related_model_name, model_name

    if relation_type in ["many-to-many", "one-to-one"]:
        column = None
    else:
        column = field.column

    return {
        "schema_name": schema_name,
        "related_schema_name": related_schema_name,
        "model_name": model_name,
        "related_model_name": related_model_name,
        "field_name": field_name,
        "related_field_name": related_field_name,
        "column": column,
        "type": internal_type,
        "relation_type": relation_type,
        "is_link_table": issubclass(field.model, LinkORM),
    }


def get_relation_type(model, field):
    if field.many_to_one:
        if model == field.model:
            return "many-to-one"
        else:
            return "one-to-many"
    elif field.one_to_many:
        return "one-to-many"
    elif field.many_to_many:
        return "many-to-many"
    elif field.one_to_one:
        return "one-to-one"
    else:
        return None


def get_queryable_field_names(model):
    fields = [field for field in model._meta.fields]
    model_relations_metadata = ModelRelations(model)

    for link_field_name, link_field in model_relations_metadata.many_to_one.items():
        fields.extend([f"{link_field_name}__{field.name}" for field in link_field.related_model._meta.fields])

    return fields


def get_selectable_field_names(model):
    fields = get_queryable_field_names(model)
    model_relations_metadata = ModelRelations(model)

    for link_field_name, link_field in model_relations_metadata.one_to_many.items():
        fields.extend([f"{link_field_name}__{field.name}" for field in link_field.related_model._meta.fields])

    return fields


def get_models_metadata():
    schema_names = ["core"] + list(_settings.instance.schema)
    metadata: Dict[str, Dict[str, ModelMetadata]] = {}
    for schema_name in schema_names:
        schema_module = importlib.import_module(f"{get_schema_module_name(schema_name)}.models")
        metadata[schema_name] = {}
        for model in schema_module.__dict__.values():
            if model.__class__.__name__ == "ModelBase" and model.__name__ not in [
                "Registry",
                "ORM",
            ]:
                metadata[schema_name].update({model.__name__: ModelMetadata(model)})
    return metadata


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


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_core", "0022_dataset_uid_feature_uid_featureset_uid_file_uid_and_more"),
    ]

    operations = []  # type: ignore


def delete_old_foreign_keys(model_name):
    print(f"deleting old foreign key columns for {model_name}")
    model_metadata = SchemaMetadata.get_models()["core"][model_name]
    # for each many_to_many, loop through foreign keys
    # for many_to_many_field in model_metadata.relations.many_to_many:
    #     add_a_new_column_foreign_keys(many_to_many_field.model)
    # for each foreign_key, add a new column with _tmp suffix
    migrations_list = []
    for foreign_key_name in model_metadata.relations.many_to_one:
        if not (model_name == "File" and foreign_key_name == "storage"):
            migrations_list.append(migrations.RemoveField(model_name, foreign_key_name))
    return migrations_list


# delete old foreign keys
for model_name in CORE_MODELS.keys():
    Migration.operations += delete_old_foreign_keys(model_name=model_name)


# turn previous primary keys into regular char fields
Migration.operations += [
    migrations.AlterField(
        model_name="dataset",
        name="uid",
        field=models.CharField(db_index=True, default=lnschema_core.ids.base62_20, max_length=20, unique=True),
    ),
    migrations.AlterField(
        model_name="datasetfeatureset",
        name="id",
        field=models.BigAutoField(primary_key=True, serialize=False),
    ),
    migrations.AlterField(
        model_name="datasetulabel",
        name="id",
        field=models.BigAutoField(primary_key=True, serialize=False),
    ),
    migrations.AlterField(
        model_name="feature",
        name="uid",
        field=models.CharField(db_index=True, default=lnschema_core.ids.base62_12, max_length=12, unique=True),
    ),
    migrations.AlterField(
        model_name="featureset",
        name="uid",
        field=models.CharField(db_index=True, default=None, max_length=20, unique=True),
    ),
    migrations.AlterField(
        model_name="file",
        name="uid",
        field=models.CharField(db_index=True, max_length=20, unique=True),
    ),
    migrations.AlterField(
        model_name="filefeatureset",
        name="id",
        field=models.BigAutoField(primary_key=True, serialize=False),
    ),
    migrations.AlterField(
        model_name="fileulabel",
        name="id",
        field=models.BigAutoField(primary_key=True, serialize=False),
    ),
    migrations.AlterField(
        model_name="modality",
        name="uid",
        field=models.CharField(db_index=True, default=lnschema_core.ids.base62_8, max_length=8, unique=True),
    ),
    migrations.AlterField(
        model_name="run",
        name="uid",
        field=models.CharField(db_index=True, default=lnschema_core.ids.base62_20, max_length=20, unique=True),
    ),
    migrations.AlterField(
        model_name="storage",
        name="uid",
        field=models.CharField(db_index=True, default=lnschema_core.ids.base62_8, max_length=8, unique=True),
    ),
    migrations.AlterField(
        model_name="transform",
        name="uid",
        field=models.CharField(db_index=True, default=None, max_length=14, unique=True),
    ),
    migrations.AlterField(
        model_name="ulabel",
        name="uid",
        field=models.CharField(db_index=True, default=lnschema_core.ids.base62_8, max_length=8, unique=True),
    ),
    migrations.AlterField(
        model_name="user",
        name="uid",
        field=models.CharField(db_index=True, default=None, max_length=8, unique=True),
    ),
]

# turn integer id fields into primary keys
for model_name, big in CORE_MODELS.items():
    Migration.operations.append(
        migrations.AlterField(
            model_name=model_name,
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False) if big else models.AutoField(primary_key=True, serialize=False),
        ),
    )


# add foreign keys back
Migration.operations += [
    migrations.AddField(
        model_name="dataset",
        name="created_by",
        field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="created_datasets", to="lnschema_core.user"),
    ),
    migrations.AddField(
        model_name="dataset",
        name="initial_version",
        field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to="lnschema_core.dataset"),
    ),
    migrations.AddField(
        model_name="dataset",
        name="run",
        field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="output_datasets", to="lnschema_core.run"),
    ),
    migrations.AddField(
        model_name="dataset",
        name="storage",
        field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name="datasets", to="lnschema_core.storage"),
    ),
    migrations.AddField(
        model_name="dataset",
        name="transform",
        field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="datasets", to="lnschema_core.transform"),
    ),
    migrations.AddField(
        model_name="feature",
        name="created_by",
        field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="created_features", to="lnschema_core.user"),
    ),
    migrations.AddField(
        model_name="feature",
        name="modality",
        field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="features", to="lnschema_core.modality"),
    ),
    migrations.AddField(
        model_name="featureset",
        name="created_by",
        field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="created_feature_sets", to="lnschema_core.user"),
    ),
    migrations.AddField(
        model_name="featureset",
        name="modality",
        field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="feature_sets", to="lnschema_core.modality"),
    ),
    migrations.AddField(
        model_name="file",
        name="created_by",
        field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="created_files", to="lnschema_core.user"),
    ),
    migrations.AddField(
        model_name="file",
        name="initial_version",
        field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to="lnschema_core.file"),
    ),
    migrations.AddField(
        model_name="file",
        name="run",
        field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="output_files", to="lnschema_core.run"),
    ),
    migrations.AddField(
        model_name="file",
        name="storage",
        field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="files", to="lnschema_core.storage"),
        preserve_default=False,
    ),
    migrations.AddField(
        model_name="file",
        name="transform",
        field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="output_files", to="lnschema_core.transform"),
    ),
    migrations.AddField(
        model_name="modality",
        name="created_by",
        field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="created_modalities", to="lnschema_core.user"),
    ),
    migrations.AddField(
        model_name="run",
        name="created_by",
        field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name="created_runs", to="lnschema_core.user"),
    ),
    migrations.AddField(
        model_name="run",
        name="report",
        field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="report_of", to="lnschema_core.file"),
    ),
    migrations.AddField(
        model_name="run",
        name="transform",
        field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name="runs", to="lnschema_core.transform"),
        preserve_default=False,
    ),
    migrations.AddField(
        model_name="storage",
        name="created_by",
        field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="created_storages", to="lnschema_core.user"),
    ),
    migrations.AddField(
        model_name="transform",
        name="created_by",
        field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="created_transforms", to="lnschema_core.user"),
    ),
    migrations.AddField(
        model_name="transform",
        name="initial_version",
        field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to="lnschema_core.transform"),
    ),
    migrations.AddField(
        model_name="transform",
        name="latest_report",
        field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="latest_report_of", to="lnschema_core.file"),
    ),
    migrations.AddField(
        model_name="transform",
        name="source_file",
        field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="source_of", to="lnschema_core.file"),
    ),
    migrations.AddField(
        model_name="ulabel",
        name="created_by",
        field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name="created_ulabels", to="lnschema_core.user"),
    ),
]


def populate_new_column_foreign_keys(model_name):
    print(f"populate new foreign key column for {model_name}")
    model_metadata = SchemaMetadata.get_models()["core"][model_name]
    migrations_list = []
    for foreign_key_name in model_metadata.relations.many_to_one:
        table = model_metadata.model._meta.db_table
        command = f"UPDATE {table} SET {foreign_key_name}_id={foreign_key_name}_id_tmp"
        migrations_list.append(migrations.RunSQL(command))
    return migrations_list


# populate temporary fields
for model_name in CORE_MODELS.keys():
    Migration.operations += populate_new_column_foreign_keys(model_name=model_name)


# fix defaults for foreign keys and nullability
Migration.operations += [
    migrations.AlterField(
        model_name="dataset",
        name="created_by",
        field=models.ForeignKey(
            default=lnschema_core.users.current_user_id, on_delete=django.db.models.deletion.PROTECT, related_name="created_datasets", to="lnschema_core.user"
        ),
    ),
    migrations.AlterField(
        model_name="feature",
        name="created_by",
        field=models.ForeignKey(
            default=lnschema_core.users.current_user_id, on_delete=django.db.models.deletion.PROTECT, related_name="created_features", to="lnschema_core.user"
        ),
    ),
    migrations.AlterField(
        model_name="featureset",
        name="created_by",
        field=models.ForeignKey(
            default=lnschema_core.users.current_user_id, on_delete=django.db.models.deletion.PROTECT, related_name="created_feature_sets", to="lnschema_core.user"
        ),
    ),
    migrations.AlterField(
        model_name="file",
        name="created_by",
        field=models.ForeignKey(
            default=lnschema_core.users.current_user_id, on_delete=django.db.models.deletion.PROTECT, related_name="created_files", to="lnschema_core.user"
        ),
    ),
    migrations.AlterField(
        model_name="file",
        name="storage",
        field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="files", to="lnschema_core.storage"),
    ),
    migrations.AlterField(
        model_name="modality",
        name="created_by",
        field=models.ForeignKey(
            default=lnschema_core.users.current_user_id, on_delete=django.db.models.deletion.PROTECT, related_name="created_modalities", to="lnschema_core.user"
        ),
    ),
    migrations.AlterField(
        model_name="run",
        name="created_by",
        field=models.ForeignKey(default=lnschema_core.users.current_user_id, on_delete=django.db.models.deletion.CASCADE, related_name="created_runs", to="lnschema_core.user"),
    ),
    migrations.AlterField(
        model_name="run",
        name="transform",
        field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="runs", to="lnschema_core.transform"),
    ),
    migrations.AlterField(
        model_name="storage",
        name="created_by",
        field=models.ForeignKey(
            default=lnschema_core.users.current_user_id, on_delete=django.db.models.deletion.PROTECT, related_name="created_storages", to="lnschema_core.user"
        ),
    ),
    migrations.AlterField(
        model_name="transform",
        name="created_by",
        field=models.ForeignKey(
            default=lnschema_core.users.current_user_id, on_delete=django.db.models.deletion.PROTECT, related_name="created_transforms", to="lnschema_core.user"
        ),
    ),
    migrations.AlterField(
        model_name="ulabel",
        name="created_by",
        field=models.ForeignKey(
            default=lnschema_core.users.current_user_id, on_delete=django.db.models.deletion.PROTECT, related_name="created_ulabels", to="lnschema_core.user"
        ),
    ),
]
