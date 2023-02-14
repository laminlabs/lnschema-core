from sqlmodel import Field


def current_user_id():
    from lndb import settings

    return settings.user.id


CreatedBy = Field(default_factory=current_user_id, foreign_key="core.user.id", index=True)
