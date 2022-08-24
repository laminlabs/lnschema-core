import secrets
import string


def base64(n_char: int) -> str:
    """Like nanoid.

    Alphabet: `string.digits + string.ascii_letters.swapcase() + "_-"`
    """
    alphabet = string.digits + string.ascii_letters.swapcase() + "_" + "-"
    id = "".join(secrets.choice(alphabet) for i in range(n_char))
    return id


def base62(n_char: int) -> str:
    """Like nanoid without hyphen and underscore."""
    alphabet = string.digits + string.ascii_letters.swapcase()
    id = "".join(secrets.choice(alphabet) for i in range(n_char))
    return id


def base26(n_char: int):
    """ASCII lowercase."""
    alphabet = string.ascii_lowercase
    id = "".join(secrets.choice(alphabet) for i in range(n_char))
    return id


def schema():
    """Schema module: 4-char base26."""
    return base26(4)


def dobject() -> str:
    """Data object: 21-char base62.

    21 characters (62**21=4e+37 possibilities) outperform UUID (2*122=5e+36).
    """
    return base62(n_char=21)


def dtransform() -> str:
    """Data transformation: 21-char base62."""
    return base62(n_char=22)


def user() -> str:
    """User: 8 base64.

    Consistent with 1M users producing 1k notebooks.
    Safe for 100k users producing 10k notebooks.

    Allows >2e14 users.

    This is one of 2 IDs that are centralized.

    Collision probability in decentralized system is:

    ======= ===========
    n_users p_collision
    ======= ===========
    100k    2e-05
    1M      2e-03
    ======= ===========
    """
    return base64(n_char=8)


def usage() -> str:
    """Usage event: 24-char base62."""
    return base62(n_char=24)


def secret() -> str:
    """Password or secret: 40-char base62."""
    return base62(n_char=40)


def instance() -> str:
    """LaminDB instance: 10-char base62.

    Collision probability is 6e-03 for 100M instances: 1M users with 100 instances/user.
    """
    return base62(n_char=10)


def storage() -> str:
    """Storage root: 10-char base62.

    Collision probability is 6e-03 for 100M storage roots: 1M users with 100
    storage roots/user.
    """
    return base62(n_char=10)


def jupynb():
    """Jupyter notebook: 12-char base62.

    Collision probability is 2e-04 for 1B notebooks: 1M users with 1k notebooks/user.

    Is the same as nbproject ID!
    """
    return base62(n_char=12)
