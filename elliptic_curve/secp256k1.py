import secrets

from .curve import EllipticCurve


#
# The curve is represented as:
#   - P:    Prime modulus of the Galois field.
#   - a, b: Weierstrass curve equation coefficients.
#           E: y**2 = x**3 + ax + b over the prime field.
#   - G:    Generator base point (x, y) coordinates.
#
size = 256
P = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1
a, b = 0, 7

Secp256k1 = EllipticCurve(a, b, P)

G = Secp256k1((
    0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798,
    0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8))


def generate_private_key():
    return secrets.randbits(size)


def get_public_key(privkey):
    return G * privkey


def generate_key_pair():
    """
    For elliptic curve cryptography:
      - a private key is a large random integer,
      - a public key is the generator point multiplied by the private key.
    """
    privkey = generate_private_key()
    pubkey = get_public_key(privkey)
    return (privkey, pubkey)
