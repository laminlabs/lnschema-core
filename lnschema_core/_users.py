from base64 import b64decode

from sqlmodel import Field


def current_user_id() -> str:
    from lndb import settings

    return settings.user.id


def current_user_id_as_int() -> int:
    str_id = current_user_id()
    return int.from_bytes(b64decode(str_id), "big")


CreatedBy = Field(default_factory=current_user_id, foreign_key="lnschema_core_user.id", index=True)
