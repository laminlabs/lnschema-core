import lamindb_setup as ln_setup
import pytest


@pytest.fixture(scope="module")
def setup_bionty_instance():
    ln_setup.init(storage="./test-bionty-db", schema="bionty")
    yield
    ln_setup.delete("test-bionty-db", force=True)


def test_migrate_check(setup_bionty_instance):
    assert ln_setup.migrate.check()


def test_system_check(setup_bionty_instance):
    ln_setup.django("check")
