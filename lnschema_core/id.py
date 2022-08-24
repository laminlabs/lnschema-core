"""IDs.

See: https://github.com/laminlabs/lamin-notes/blob/main/docs/2022/ids.ipynb

Base generators:

.. autosummary::
   :toctree: .

   base26
   base62
   base64

Entity-related generators:

.. autosummary::
   :toctree: .

   schema_module
   user
   dobject
   dtransform
   secret
   usage
   storage
   instance
   jupynb
"""

import secrets
import string


def base64(n_char: int) -> str:
    """Like nanoid.

    Alphabet: `string.digits + string.ascii_letters.swapcase() + "_-"`
    """
    base62 = string.digits + string.ascii_letters.swapcase() + "_" + "-"
    id = "".join(secrets.choice(base62) for i in range(n_char))
    return id


def base62(n_char: int) -> str:
    """Like nanoid without hyphen and underscore."""
    base62 = string.digits + string.ascii_letters.swapcase()
    id = "".join(secrets.choice(base62) for i in range(n_char))
    return id


id_base62 = base62  # backward compat


def base26(n_char: int):
    """ASCII lowercase."""
    base26 = string.ascii_lowercase
    id = "".join(secrets.choice(base26) for i in range(n_char))
    return id


id_base26 = base62  # backward compat


def schema_module():
    """Schema module: 4-char base26."""
    return id_base26(4)


id_schema_module = schema_module  # backward compat


def dobject() -> str:
    """Data object: 21-char base62.

    21 characters (62**21=4e+37 possibilities) outperform UUID (2*122=5e+36).
    """
    return id_base62(n_char=21)


id_dobject = dobject  # backward compat


def dtransform() -> str:
    """Data transformation: 21-char base62."""
    return id_base62(n_char=22)


id_dtransform = dtransform  # backward compat


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


id_user = user  # backward compat


def usage() -> str:
    """Usage event: 24-char base62."""
    return id_base62(n_char=24)


id_usage = usage  # backward compat


def secret() -> str:
    """Password or secret: 40-char base62."""
    return id_base62(n_char=40)


id_secret = secret  # backward compat


def instance() -> str:
    """LaminDB instance: 10-char base62.

    Collision probability is 6e-03 for 100M instances: 1M users with 100 instances/user.
    """
    return id_base62(n_char=10)


id_instance = instance  # backward compat


def storage() -> str:
    """Storage root: 10-char base62.

    Collision probability is 6e-03 for 100M storage roots: 1M users with 100
    storage roots/user.
    """
    return id_base62(n_char=10)


id_storage = storage  # backward compat


def jupynb():
    """Jupyter notebook: 12-char base62.

    Collision probability is 2e-04 for 1B notebooks: 1M users with 1k notebooks/user.

    Is the same as nbproject ID!
    """
    # https://github.com/laminlabs/lamin-notes/blob/main/docs/2022/ids.ipynb
    return id_base62(n_char=12)
