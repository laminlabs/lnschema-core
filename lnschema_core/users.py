user_id_cache = {}


def current_user_id() -> int:
    from lamindb_setup import settings

    from lnschema_core.models import User

    if settings._instance_exists:
        if settings.instance.identifier not in user_id_cache:
            user_id_cache[settings.instance.identifier] = User.objects.get(uid=settings.user.uid).id
        return user_id_cache[settings.instance.identifier]
    else:
        return User.objects.get(uid=settings.user.uid).id
