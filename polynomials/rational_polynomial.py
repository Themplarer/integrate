from decimal import Decimal
from fractions import Fraction

from polynomials.polynomial import Polynomial


def _convert_to_rational_pol(p):
    if all(map(is_rational, p.coeffs)):
        return RationalPolynomial(p.coeffs, p.variable)

    return p


def is_rational(number):
    return isinstance(number, int) or isinstance(number, float) or \
           isinstance(number, Decimal) or isinstance(number, Fraction)


class RationalPolynomial(Polynomial):
    """Описывает многочлен над полем рациональных чисел"""

    def __init__(self, coeffs_by_powers_desc, variable='x'):
        if not all(map(is_rational, coeffs_by_powers_desc)):
            raise ValueError('coeffs are not rationals!')

        super().__init__(coeffs_by_powers_desc, variable)

    def __add__(self, other):
        return _convert_to_rational_pol(self._add_signed(other, True))

    def __sub__(self, other):
        return _convert_to_rational_pol(self._add_signed(other, False))

    def __mul__(self, other):
        if isinstance(other, Fraction):
            return RationalPolynomial([other * i for i in self.coeffs],
                                      self.variable)

        return _convert_to_rational_pol(super().__mul__(other))

    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, Fraction):
            return RationalPolynomial([i / other for i in self.coeffs],
                                      self.variable)

        raise ValueError('impossible to divide polynomial by '
                         f'{type(other).__name__}!')

    def __floordiv__(self, other):
        return self.__truediv__(other)

    def __divmod__(self, other):
        div, mod = super().__divmod__(other)
        return _convert_to_rational_pol(div), _convert_to_rational_pol(mod)

    def __eq__(self, other):
        if isinstance(other, Fraction):
            return self.power == 0 and self.coeffs[0] == other

        return super().__eq__(other)

    def _add_signed(self, other, is_adding):
        if isinstance(other, int) or isinstance(other, Fraction):
            new_coeffs = list(self.coeffs)
            new_coeffs[0] += other if is_adding else -other
            return RationalPolynomial(new_coeffs, self.variable)

        return super()._add_signed(other, is_adding)
