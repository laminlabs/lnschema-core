user_id_cache = {}


def current_user_id() -> int:
    from lamindb_setup import settings

    from lnschema_core.models import User

    def query_user_id():
        try:
            return User.objects.get(uid=settings.user.uid).id
        except Exception:
            return 1

    if settings._instance_exists:
        if settings.instance.slug not in user_id_cache:
            user_id_cache[settings.instance.slug] = query_user_id()
        return user_id_cache[settings.instance.slug]
    else:
        return query_user_id()
