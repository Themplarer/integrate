import math
from functools import total_ordering


def reduce(n, d):
    num = abs(n)
    den = abs(d)

    gcd = math.gcd(num, den)
    num //= gcd
    den //= gcd

    if (n < 0) ^ (d < 0):
        num *= -1

    return num, den


class RationalFunction:
    def __init__(self, numerator, denominator):
        if not isinstance(numerator, int) or not isinstance(denominator, int):
            raise ValueError('rational must be pair of 2 ints')

        if not denominator:
            raise ZeroDivisionError('denominator must not be equal to 0')

        self.numerator, self.denominator = reduce(numerator, denominator)

    def __add__(self, other):
        f = self._check_argument(other)
        return RationalFunction(self.numerator * f.denominator +
                                f.numerator * self.denominator,
                                self.denominator * f.denominator)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        f = self._check_argument(other)
        return RationalFunction(self.numerator * f.denominator -
                                f.numerator * self.denominator,
                                self.denominator * f.denominator)

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        f = self._check_argument(other)
        return RationalFunction(self.numerator * f.numerator,
                                self.denominator * f.denominator)

    def __rmul__(self, other):
        return self * other

    def __floordiv__(self, other):
        f = self._check_argument(other)
        return RationalFunction(self.numerator * f.denominator,
                                self.denominator * f.numerator)

    def __truediv__(self, other):
        return self.__floordiv__(other)

    def __pos__(self):
        return self

    def __neg__(self):
        return self * (-1)

    def __abs__(self):
        return RationalFunction(abs(self.numerator), self.denominator)

    def __int__(self):
        return self.numerator // self.denominator

    def __float__(self):
        return self.numerator / self.denominator

    def __str__(self):
        if self.numerator % self.denominator == 0:
            return str(self.numerator)

        return f'{self.numerator}/{self.denominator}'

    def __eq__(self, other):
        f = self._check_argument(other)
        return self.numerator * f.denominator == self.denominator * f.numerator

    def __lt__(self, other):
        f = self._check_argument(other)
        return self.numerator * f.denominator < self.denominator * f.numerator

    @staticmethod
    def _check_argument(arg):
        f = arg

        if isinstance(f, int):
            f = RationalFunction(f, 1)

        if not isinstance(f, RationalFunction):
            raise ArithmeticError(f'cannot add {type(f).__name__} to rational!')

        return f
