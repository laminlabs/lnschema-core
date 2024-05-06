from lamin_utils import logger

user_id_cache = {}


def current_user_id() -> int:
    # Internal function, do not use directly due to the try & except block
    # Instead, use lamindb_setup.settings.user.id
    from lamindb_setup import settings

    from lnschema_core.models import User

    def query_user_id():
        try:
            return User.objects.get(uid=settings.user.uid).id
        except Exception:
            logger.warning(
                "Couldn't retrieve user id (the `created_by` field couldn't be set correctly).\n"
                "Your user is not yet part of the User registry of this instance. Run\n"
                "from lamindb_setup._init_instance import register_user\n"
                "register_user(ln.setup.settings.user)"
            )
            # This is needed when first creating the instance during migrations
            return 1

    if settings._instance_exists:
        if settings.instance.slug not in user_id_cache:
            user_id_cache[settings.instance.slug] = query_user_id()
        return user_id_cache[settings.instance.slug]
    else:
        return query_user_id()
