"""IDs.

See: https://github.com/laminlabs/lamin-notes/blob/main/docs/2022/ids.ipynb

Base generators:

.. autosummary::
   :toctree: .

   base26
   base62
   Base62
   base64

For example, 8 base62 characters:

======= ===========
n_rows  p_collision
======= ===========
100k    2e-05
1M      2e-03
======= ===========

20 base62 characters (62**20=7e+35) roughly matches UUID (2*122=5e+36).
"""
# Some IDs got updated on 2023-02-14 to be multiples of 4
# for matching byte representation, should we ever go there.
import secrets
import string


def base64(n_char: int) -> str:
    """Like nanoid."""
    alphabet = string.digits + string.ascii_letters.swapcase() + "_" + "-"
    id = "".join(secrets.choice(alphabet) for i in range(n_char))
    return id


def base62(n_char: int) -> str:
    """Like nanoid without hyphen and underscore."""
    alphabet = string.digits + string.ascii_letters.swapcase()
    id = "".join(secrets.choice(alphabet) for i in range(n_char))
    return id


# this cannot be serialized by Django,
# hence, see below
class Base62:
    def __init__(self, n_char: int):
        self.n_char = n_char

    def __call__(self):
        return base62(self.n_char)


def base26(n_char: int):
    """ASCII lowercase."""
    alphabet = string.ascii_lowercase
    id = "".join(secrets.choice(alphabet) for i in range(n_char))
    return id


def base62_4() -> str:
    return base62(4)


def base62_8() -> str:
    return base62(8)


def base62_12() -> str:
    return base62(12)


def base62_16() -> str:
    return base62(16)


def base62_20() -> str:
    return base62(20)


def base62_24() -> str:
    return base62(24)
