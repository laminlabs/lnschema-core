def current_user_id() -> str:
    from lamindb_setup import settings

    return settings.user.id


def current_user_id_as_int() -> int:
    from lamindb_setup import settings

    return settings.user.get_id_as_int()
