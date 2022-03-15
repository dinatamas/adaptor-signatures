#
# https://tlu.tarilabs.com/cryptography/introduction-schnorr-signatures
# https://tlu.tarilabs.com/cryptography/The_MuSig_Schnorr_Signature_Scheme
# https://asecuritysite.com/encryption/schnorr_test3
#
from dataclasses import dataclass
from functools import cached_property

from elliptic_curve.secp256k1 import Secp256k1, G, P, order
from protocol.utils import i2b, b2i, sha256, ptsum


@dataclass
class MuSigSession:
    # Stored attributes:
    x: int                    = None  # own private key
    X: Secp256k1.Point        = None  # own public key
    Xs: list[Secp256k1.Point] = None  # all public keys
    r: int                    = None  # own private nonce
    R: Secp256k1.Point        = None  # own public nonce
    Rs: list[Secp256k1.Point] = None  # all public nonces
    ts: list[bytes]           = None  # all commitments (in same order as Rs)

    # Calculated attributes:
    # Xc: Secp256k1.Point  - common public key
    # t: bytes             - own commitment
    # Rc: Secp256k1.Point  - common public nonce

    # Helper attributes:
    # L: bytes  - sha256(Xs)
    # a: int    - sha256(L + X)
    # c: int    - sha256(Xc + Rc + msg)

    # Caution!
    # - Do not share your public nonce before receiving all commitments!
    # - Received commitments should match public nonces! (auto-verified)
    # - Do NOT reuse values for r and R!

    @cached_property
    def L(self):
        return sha256(b''.join(i2b(X[0]) for X in sorted(self.Xs)))

    @cached_property
    def a(self):
        return b2i(sha256(self.L + i2b(self.X[0])))

    @cached_property
    def Xc(self):
        return ptsum(b2i(sha256(self.L + i2b(X[0]))) * X for X in sorted(self.Xs))

    @cached_property
    def t(self):
        return sha256(i2b(self.R[0]))

    @cached_property
    def Rc(self):
        for i in range(len(self.ts)):
            assert self.ts[i] == sha256(i2b(self.Rs[i][0]))
        return ptsum(self.Rs)

    def c(self, msg):
        return b2i(sha256(i2b(self.Xc[0]) + i2b(self.Rc[0]) + msg))

    def sign(self, msg):
        return (self.r + self.c(msg) * self.a * self.x) % order

    def verify(self, msg, signature):
        return G * signature == self.Rc + self.Xc * self.c(msg)


def sum_musig_signatures(signatures):
    return sum(signatures) % order
