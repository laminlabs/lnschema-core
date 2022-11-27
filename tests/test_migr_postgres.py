from lndb_setup._test_migrate import test_migrate


def test_migrate_postgres():
    results = test_migrate("lnschema_core", n_instances=1, dialect_name="postgresql")
    print(results)
    # if "migrate-failed" in results:
    #     raise RuntimeError("Migration failed.")
