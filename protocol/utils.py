#
# Utility and convenience functions.
#
from functools import reduce
import hashlib


def i2b(i):
    """ Integer to bytes. """
    return i.to_bytes(32, byteorder='big')


def b2i(b):
    """ Bytes to integer. """
    return int.from_bytes(b, byteorder='big')


def sha256(*args):
    hasher = hashlib.sha256()
    for arg in args:
        hasher.update(arg)
    return hasher.digest()
