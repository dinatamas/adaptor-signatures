"""
https://jeremykun.com/2014/02/16/elliptic-curves-as-algebraic-structures/
https://cryptobook.nakov.com/asymmetric-key-ciphers/elliptic-curve-cryptography-ecc
https://onyb.gitbook.io/secp256k1-python/introduction
"""
from .field import PrimeField


class EllipticCurve:
    """ Weierstrass elliptic curve. """

    def __init__(self, a, b, P):
        self.field = field = PrimeField(P)
        self.a = field(a)
        self.b = field(b)
        # Point at Infinity: additive neutral element.
        # Represented as a point with two None coordinates.
        # This is a singleton, and will be instantiated later.
        self.O = None
        
        class Point(tuple):
            """ https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication """

            def __new__(cls, x, y):
                if x is None and y is None:
                    if self.O is None:
                        self.O = super().__new__(cls, (None, None))
                    return self.O
                x, y = field(x), field(y)
                return super().__new__(cls, (x, y))

            def __add__(p, q):
                if p is self.O:
                    return q
                if q is self.O:
                    return p
                if p == -q:
                    return self.O
                if p == q:
                    delta = (3 * p[0] ** 2 + a) / (2 * p[1])
                else:
                    delta = (q[1] - p[1]) / (q[0] - p[0])
                x = delta ** 2 - p[0] - q[0]
                y = delta * (p[0] - x) - p[1]
                return p.__class__(x, y)

            def __mul__(p, n):
                if n == 0:
                    return self.O
                if p is self.O:
                    return self.O
                res = p
                for bit in bin(n)[3:]:
                    res += res
                    if bit == '1':
                        res += p
                return res

            def __neg__(p):
                if p is self.O:
                    raise ZeroDivisionError('Cannot negate the Point at Infinity.')
                return p.__class__(p[0], -p[1])

            def __rmul__(p, n):
                return p.__mul__(n)

        self.Point = Point
        self.O = Point(None, None)

    def __call__(self, x, y):
        return self.Point(x, y)
