from sqlmodel import Field


def current_user_id() -> str:
    from lamindb_setup import settings

    return settings.user.id


def current_user_id_as_int() -> int:
    from lamindb_setup import settings

    return settings.user.get_id_as_int()


CreatedBy = Field(default_factory=current_user_id, foreign_key="lnschema_core_user.id", index=True)
