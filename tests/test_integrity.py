import lamindb_setup as ln_setup
import pytest


def test_migrate_check(setup_instance):
    assert ln_setup.migrate.check()


def test_system_check(setup_instance):
    ln_setup.django("check")
