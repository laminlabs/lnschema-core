# Generated by Django 4.2.5 on 2023-10-11 13:34

from pathlib import Path

import lamindb_setup
import lamindb_setup as ln_setup
from django.db import migrations

import lnschema_core.models

CORE_MODELS = {
    # sorted by topology of foreign keys
    "User": False,
    "Transform": False,
    "Run": True,
    "Storage": False,
    "Modality": False,
    "Feature": False,
    "FeatureSet": False,
    "ULabel": False,
    "File": False,
    "Dataset": False,
}


def import_registry(registry, directory, connection):
    import pandas as pd

    table_name = registry._meta.db_table
    df = pd.read_parquet(directory / f"{table_name}.parquet")
    old_foreign_key_columns = [column for column in df.columns if column.endswith("_old")]
    for column in old_foreign_key_columns:
        df.drop(column, axis=1, inplace=True)
    df.to_sql(table_name, connection, if_exists="append", index=False)


def import_db(apps, schema_editor):
    # import data from parquet files
    directory = Path(f"./lamindb_export/{ln_setup.settings.instance.identifier}/")
    if directory.exists():
        response = input(
            "\n\nHave you deleted or archived your old instance (sqlite file or postgres database) and re-initialized your instance? Only if so, proceed to import data from"
            f" the parquet files: {directory}? Otherwise hit 'n' and see instructions. (y/n)\n"
        )
        if response != "y":
            print(
                "Please delete or archive your current database (sqlite file or postgres database) and re-initialize your instance using lamin init and the same account,"
                " instance name, schema, db & storage settings; you can see them using: lamin info"
            )
            raise SystemExit
        from sqlalchemy import create_engine

        engine = create_engine(ln_setup.settings.instance.db, echo=False)
        with engine.begin() as connection:
            if ln_setup.settings.instance.dialect == "postgresql":
                connection.execute("SET CONSTRAINTS ALL DEFERRED;")
            for model_name in CORE_MODELS.keys():
                registry = getattr(lnschema_core.models, model_name)
                import_registry(registry, directory, connection)
                many_to_many_names = [field.name for field in registry._meta.many_to_many]
                for many_to_many_name in many_to_many_names:
                    link_orm = getattr(registry, many_to_many_name).through
                    import_registry(link_orm, directory, connection)


class Migration(migrations.Migration):
    dependencies = [
        ("lnschema_core", "0001_initial_squashed_0023"),
    ]

    operations = [
        migrations.RunPython(import_db, reverse_code=migrations.RunPython.noop),
    ]


schemas = lamindb_setup.settings.instance.schema
if "bionty" in schemas:
    Migration.dependencies.append(("lnschema_bionty", "0016_export_legacy_data"))
if "lamin1" in schemas:
    Migration.dependencies.append(("lnschema_lamin1", "0012_export_legacy_data"))