from lndb_schema_core import id


def test_id():
    assert len(id.id_dobject()) == 21
    assert len(id.id_user()) == 8
    assert len(id.id_secret()) == 40
    assert len(id.id_track()) == 24
    assert len(id.id_instance()) == 12
