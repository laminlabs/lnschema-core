import pytest
import sqlalchemy as sa


@pytest.fixture
def alembic_engine():
    return sa.create_engine("sqlite:///")
