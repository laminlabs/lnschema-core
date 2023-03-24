# Some IDs got updated on 2023-02-14 to be multiples of 4
# for matching byte representation, should we ever go there.
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


def file() -> str:
    """Data object: 20 base62.

    20 characters (62**20=7e+35 possibilities) roughly matches UUID (2*122=5e+36).

    Can be encoded as 15 bytes.
    """
    return base62(n_char=20)


def folder() -> str:
    """Data folder: 20 base62."""
    return base62(n_char=20)


def run() -> str:
    """Data transformation: 20 base62."""
    return base62(n_char=20)


def user() -> str:
    """User: 8 base62.

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
    return base62(n_char=8)


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
    """LaminDB instance: 12 base62.

    Collision probability is 2e-04 for 1B instances: 1M users with 1k instances/user.
    """
    return base62(n_char=12)


def storage() -> str:
    """Storage root: 8 base62."""
    return base62(n_char=8)


def pipeline() -> str:
    """Pipeline: 8 base62."""
    return base62(n_char=8)


def notebook():
    """Jupyter notebook: 12 base62.

    Collision probability is 2e-04 for 1B notebooks: 1M users with 1k notebooks/user.

    Is the same as nbproject ID!
    """
    return base62(n_char=12)
