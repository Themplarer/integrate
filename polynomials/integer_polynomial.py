from decimal import Decimal
from fractions import Fraction

from polynomials.rational_polynomial import RationalPolynomial


def _convert_to_int_pol(p):
    if all(map(is_int, p.coeffs)):
        return IntegerPolynomial(p.coeffs, p.variable)

    return p


def is_int(number):
    return isinstance(number, int) or \
           isinstance(number, float) and number.is_integer() or \
           isinstance(number, Decimal) and \
           number.as_integer_ratio()[1] == 1 or \
           isinstance(number, Fraction) and number.as_integer_ratio()[1] == 1


class IntegerPolynomial(RationalPolynomial):
    """Описывает многочлен над полем целых чисел"""

    def __init__(self, coeffs_by_powers_desc, variable='x'):
        if not all(map(is_int, coeffs_by_powers_desc)):
            raise ValueError('coeffs are not integers!')

        super().__init__(coeffs_by_powers_desc, variable)

    def __add__(self, other):
        return _convert_to_int_pol(self._add_signed(other, True))

    def __sub__(self, other):
        return _convert_to_int_pol(self._add_signed(other, False))

    def __mul__(self, other):
        return _convert_to_int_pol(super().__mul__(other))

    def __divmod__(self, other):
        div, mod = super().__divmod__(other)
        return _convert_to_int_pol(div), _convert_to_int_pol(mod)

    def __int__(self):
        if self.power == 0:
            return self.coeffs[0]

        raise ValueError('cannot convert polynomial to int!')

    def __eq__(self, other):
        if isinstance(other, int):
            return self.power == 0 and int(self) == other

        return super().__eq__(other)

    def _add_signed(self, other, is_adding):
        if isinstance(other, int):
            new_coeffs = list(self.coeffs)
            new_coeffs[0] += other if is_adding else -other
            return IntegerPolynomial(new_coeffs, self.variable)

        return super()._add_signed(other, is_adding)
