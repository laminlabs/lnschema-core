from lndb_setup._test_migrate import migrate_test
from pytest_alembic.tests import (  # noqa  # is automatically run
    test_model_definitions_match_ddl,
)


def test_migrate_sqlite():
    results = migrate_test("lnschema_core", n_instances=1, dialect_name="sqlite")
    if "migrate-failed" in results:
        raise RuntimeError("Migration failed.")


def test_migrate_postgres():
    results = migrate_test("lnschema_core", n_instances=1, dialect_name="postgresql")
    print(results)
    # if "migrate-failed" in results:
    #     raise RuntimeError("Migration failed.")
