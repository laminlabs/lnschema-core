from lndb_setup._test_migrate import migrate_test


def test_migrate_sqlite():
    results = migrate_test("lnschema_core", n_instances=1, dialect_name="sqlite")
    if "migrate-failed" in results:
        raise RuntimeError("Migration failed.")
