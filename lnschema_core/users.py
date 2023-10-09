user_id_cache = {}


def current_user_id() -> int:
    from lamindb_setup import settings

    if settings.instance.id not in user_id_cache:
        from lnschema_core.models import User

        user_id_cache[settings.instance.id] = User.objects.get(uid=settings.user.id).id
    return user_id_cache[settings.instance.id]
