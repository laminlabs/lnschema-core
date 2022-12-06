import pytest
import sqlalchemy as sa
from pytest_alembic.config import Config


@pytest.fixture
def alembic_config():
    # currently have to provide script location as it there is no
    # way to pass a name argument
    return Config(
        config_options=dict(
            config_file_name="lnschema_core/alembic.ini",
            script_location="lnschema_core/migrations",
        ),
    )


@pytest.fixture
def alembic_engine():
    return sa.create_engine("sqlite:///testdb/testdb.lndb")
