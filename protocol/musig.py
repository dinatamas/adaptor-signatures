"""
https://asecuritysite.com/encryption/schnorr_test3
https://github.com/bitcoin/bips/blob/master/bip-0340/reference.py
"""
from elliptic_curve.secp256k1 import Secp256k1, G, order
from protocol.utils import b2i, p2b, sha256


def _aggregate_permanent_public_keys(Xs):
    """Given a list of permanent public keys, return the common key."""
    L = sha256(b''.join(p2b(X) for X in Xs))
    return sum((b2i(sha256(L + p2b(X))) * X for X in Xs), start=Secp256k1.O)


def _aggregate_nonce_public_keys(Rs):
    """Given a list of nonce public keys, return the common key."""
    return sum(Rs, start=Secp256k1.O)


def sign_message(msg, x, X, Xs, r, R, Rs):
    """
    Generate an invididual signature that will be part of a multi-signature.

    Arguments:
      - msg: The message to be signed.
      - x: Permanent private key.
      - X: Permanent public key.
      - Xs: List of the permanent public keys of all signing parties.
      - r: Nonce private key.
      - R: Nonce public key.
      - Rs: List of the nonce public keys of all signing parties.
    """
    XC = _aggregate_permanent_public_keys(Xs)
    RC = _aggregate_nonce_public_keys(Rs)

    # Generate the signature.
    L = sha256(b''.join(p2b(X) for X in Xs))
    a = b2i(sha256(L + p2b(X)))
    c = b2i(sha256(p2b(XC) + p2b(RC) + msg))
    return (r + c * a * x) % order


def verify_signature(msg, sig, Xs, Rs, offset=Secp256k1.O):
    """
    Verifies that a multi-signature is valid for the given message.

    Arguments:
      - msg: The message corresponding to the signature.
      - sig: The signature to be verified.
      - Xs: List of the permanent public keys of all signing parties.
      - Rs: List of the nonce public keys of all signing parties.
      - offset: The public offset to tweak the signature with.
    """
    XC = _aggregate_permanent_public_keys(Xs)
    RC = _aggregate_nonce_public_keys(Rs)

    # Validate the signature.
    c = b2i(sha256(p2b(XC) + p2b(RC) + msg))
    return G * sig == offset + RC + XC * c
