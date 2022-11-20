#
# Utility and convenience functions.
#
from functools import reduce
import hashlib


def b2i(b):
    """ Bytes to integer. """
    return int.from_bytes(b, byteorder='big')


def i2b(i):
    """ Integer to bytes. """
    return i.to_bytes(32, byteorder='big')


# How we represent points as a byte sequence is mostly up to us. The only
# important thing is that the method remains consistent for all parties.
# In practice, points are often 'compressed' into just their X coorindate
# and a parity bit for the Y coordinate. The 'decompression' step requires
# the calculation of a modular square root (Tonelli-Shanks algorithm).
def p2b(p):
    """ Point to bytes. """
    return i2b(p[0]) + i2b(p[1])


def sha256(*args):
    hasher = hashlib.sha256()
    for arg in args:
        hasher.update(arg)
    return hasher.digest()
