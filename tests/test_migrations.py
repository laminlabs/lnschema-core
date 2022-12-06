import pytest
from alembic.autogenerate.api import AutogenContext
from alembic.autogenerate.render import _render_cmd_body
from lndb_setup._test_migrate import migrate_test
from pytest_alembic.plugin.error import AlembicTestFailure


@pytest.mark.alembic
def test_model_definitions_match_ddl(alembic_runner):
    # this function is largely copied from the
    # MIT licensed https://github.com/schireson/pytest-alembic
    """Assert that the state of the migrations matches the state of the models.

    In general, the set of migrations in the history should coalesce into DDL
    which is described by the current set of models. Therefore, a call to
    `revision --autogenerate` should always generate an empty migration (e.g.
    find no difference between your database (i.e. migrations history) and your
    models).
    """

    def verify_is_empty_revision(migration_context, __, directives):
        script = directives[0]

        migration_is_empty = script.upgrade_ops.is_empty()
        if not migration_is_empty:
            autogen_context = AutogenContext(migration_context)
            rendered_upgrade = _render_cmd_body(script.upgrade_ops, autogen_context)

            if not migration_is_empty:
                raise AlembicTestFailure(
                    "The models describing the DDL of your database are out of sync"
                    " with the set of steps described in the revision history. This"
                    " usually means that someone has made manual changes to the"
                    " database's DDL, or some model has been changed without also"
                    " generating a migration to describe that change.",
                    context=[
                        (
                            "The upgrade which would have been generated would look"
                            " like",
                            rendered_upgrade,
                        )
                    ],
                )

    alembic_runner.generate_revision(
        message="test revision",
        autogenerate=True,
        prevent_file_generation=True,
        process_revision_directives=verify_is_empty_revision,
    )


def test_migrate_sqlite():
    results = migrate_test("lnschema_core", n_instances=1, dialect_name="sqlite")
    if "migrate-failed" in results:
        raise RuntimeError("Migration failed.")


# def test_migrate_postgres():
#     results = migrate_test("lnschema_core", n_instances=1, dialect_name="postgresql")
#     print(results)
#     # if "migrate-failed" in results:
#     #     raise RuntimeError("Migration failed.")
