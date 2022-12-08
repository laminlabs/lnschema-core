import yaml  # type: ignore
from lndb_setup._test_migrate import migrate_test, model_definitions_match_ddl

with open("./lamin-project.yaml") as f:
    package_name = yaml.safe_load(f)["package_name"]


def test_model_definitions_match_ddl_postgres():
    model_definitions_match_ddl(package_name, dialect_name="postgres")


def test_migrate_sqlite():
    results = migrate_test(package_name, n_instances=1, dialect_name="sqlite")
    if "migrate-failed" in results:
        raise RuntimeError("Migration failed.")


# def test_migrate_postgres():
#     results = migrate_test(package_name, n_instances=1, dialect_name="postgresql")
#     if "migrate-failed" in results:
#          raise RuntimeError("Migration failed.")
