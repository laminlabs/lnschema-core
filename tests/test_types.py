from lnschema_core.types import VisibilityChoice


def test_visibility_choice():
    assert VisibilityChoice.default == 1
    assert VisibilityChoice.hidden == 0
    assert VisibilityChoice.trash == -1
