class PrimeField:
    def __init__(self, p):
        self.p = p

        class PrimeFieldElement(int):
            """
            https://en.wikipedia.org/wiki/Modular_arithmetic
            https://en.wikipedia.org/wiki/Finite_field_arithmetic
            https://en.wikipedia.org/wiki/Modular_multiplicative_inverse

            Compare dir(int) with https://docs.python.org/3/reference/datamodel.html
            """
            def __new__(cls, n):
                return super().__new__(cls, n % p)

            def __add__(self, rhs):
                return self.__class__(super().__add__(rhs))

            def __floordiv__(self, rhs):
                return self / rhs

            def __mul__(self, rhs):
                return self.__class__(super().__mul__(rhs))

            def __neg__(self):
                return self.__class__(pow(self, -1))

            def __pow__(self, rhs, _=None):
                return self.__class__(super().__pow__(rhs, p))

            def __radd__(self, lhs):
                return self.__class__(super().__radd__(lhs))

            def __rfloordiv__(self, lhs):
                return lhs / self

            def __rmul__(self, lhs):
                return self.__class__(super().__rmul__(lhs))

            def __rsub__(self, lhs):
                return self.__class__(super().__rsub__(lhs))

            def __rtruediv__(self, lhs):
                return self.__class__(lhs * pow(self, -1, p))

            def __sub__(self, rhs):
                return self.__class__(super().__sub__(rhs))

            def __truediv__(self, rhs):
                return self.__class__(self * pow(rhs, -1, p))

        self.PrimeFieldElement = PrimeFieldElement

    def __call__(self, n):
        return self.PrimeFieldElement(n)
