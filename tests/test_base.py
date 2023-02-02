from lnschema_core import DObject
from lnschema_core.dev import id


def test_id():
    assert len(id.dobject()) == 21
    assert len(id.user()) == 8
    assert len(id.secret()) == 40
    assert len(id.usage()) == 24
    assert len(id.instance()) == 10


def test_filekey():
    assert "_filekey" in DObject.__table__.columns.keys()
