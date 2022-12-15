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
    """Schema module: 4 base26."""
    return base26(4)


def dobject() -> str:
    """Data object: 21 base62.

    21 characters (62**21=4e+37 possibilities) outperform UUID (2*122=5e+36).
    """
    return base62(n_char=21)


def dset() -> str:
    """Data set: 21 base62."""
    return base62(n_char=21)


def run() -> str:
    """Data transformation: 21 base62."""
    return base62(n_char=21)


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


def project() -> str:
    """Project: 8 base62."""
    return base62(n_char=8)


def usage() -> str:
    """Usage event: 24 base62."""
    return base62(n_char=24)


def secret() -> str:
    """Password or secret: 40 base62."""
    return base62(n_char=40)


def instance() -> str:
    """LaminDB instance: 10 base62.

    Collision probability is 6e-03 for 100M instances: 1M users with 100 instances/user.
    """
    return base62(n_char=10)


def storage() -> str:
    """Storage root: 10 base62.

    Collision probability is 6e-03 for 100M storage roots: 1M users with 100
    storage roots/user.
    """
    return base62(n_char=10)


def pipeline() -> str:
    """Pipeline: 9 base62.

    Collision probability is low for 10M pipelines: 1M users with 10 pipelines/user.
    """
    return base62(n_char=9)


def notebook():
    """Jupyter notebook: 12 base62.

    Collision probability is 2e-04 for 1B notebooks: 1M users with 1k notebooks/user.

    Is the same as nbproject ID!
    """
    return base62(n_char=12)
