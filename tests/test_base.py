from lnschema_core import File
from lnschema_core.dev import id


def test_id():
    assert len(id.file()) == 20
    assert len(id.user()) == 8
    assert len(id.secret()) == 40
    assert len(id.usage()) == 24
    assert len(id.instance()) == 12


def test_objectkey():
    assert "_objectkey" in File.__table__.columns.keys()
