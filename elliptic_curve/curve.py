from .field import PrimeField


class EllipticCurve:
    """ Weierstrass elliptic curve. """

    def __init__(self, a, b, P):
        self.field = field = PrimeField(P)
        self.a = field(a)
        self.b = field(b)

        class Point(tuple):
            """ https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication """

            def __new__(cls, x, y):
                x, y = field(x), field(y)
                return super().__new__(cls, (x, y))

            def __add__(p, q):
                if p == q:
                    delta = (3 * p[0] ** 2 + a) / (2 * p[1])
                else:
                    delta = (q[1] - p[1]) / (q[0] - p[0])
                x = delta ** 2 - p[0] - q[0]
                y = delta * (p[0] - x) - p[1]
                return p.__class__(x, y)

            def __mul__(p, n):
                res = p
                for bit in bin(n)[3:]:
                    res += res
                    if bit == '1':
                        res += p
                return res

        self.cls = Point

    def __call__(self, p):
        return self.cls(*p)
