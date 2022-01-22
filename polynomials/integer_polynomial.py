import re
from decimal import Decimal
from fractions import Fraction

from polynomials.rational_polynomial import RationalPolynomial

_monom_regexp = re.compile(
    r'((?P<coef>-?\d+)*(\*?(?P<var>[A-Za-z])((?P<powersymbol>\^|\*\*)'
    r'(?P<power>\d*))?)?)')


def _convert_to_int_pol(p):
    if all(map(is_int, p.coeffs)):
        return IntegerPolynomial(p.coeffs, p.variable)

    return p


def parse(poly, variable='x'):
    all_letters = set(filter(lambda l: l.isalpha(), poly))
    if any(all_letters.difference(variable)):
        raise ValueError('can only parse a polynomial with one variable: '
                         f'{variable}')

    if variable not in all_letters:
        return IntegerPolynomial([eval(poly)], variable)

    brackets_balance = 0
    for i in range(len(poly)):
        index = -i - 1
        symbol = poly[index]

        if symbol == ')':
            brackets_balance += 1
        elif symbol == '(':
            brackets_balance -= 1
        elif brackets_balance == 0 and i < len(poly) - 1 and \
                (symbol in {'+', '-'}):
            left = parse(poly[:index], variable)
            right = parse(poly[index + 1:], variable)
            return left + right if symbol == '+' else left - right

    if brackets_balance:
        lost_bracket = '(' if brackets_balance > 0 else ')'
        raise AttributeError('bad brackets configuration: you have lost '
                             f'{lost_bracket} somewhere')

    brackets_balance = 0
    for i in range(len(poly)):
        index = -i - 1
        symbol = poly[index]

        if symbol == ')':
            brackets_balance += 1
        elif symbol == '(':
            brackets_balance -= 1
        elif brackets_balance == 0 and symbol == '*':
            left = parse(poly[:index], variable)
            right = parse(poly[index + 1:], variable)
            return left * right

    if poly[0] == '(' and poly[-1] == ')':
        return parse(poly[1:-1], variable)

    m = _monom_regexp.match(poly)
    if not m:
        raise AttributeError('extremely bad :(')

    power = m.group('power')
    coef = m.group('coef')
    var = m.group('var')

    if not power:
        power = 1 if var else 0

    if not coef:
        coef = 1

    return IntegerPolynomial([0] * (int(power)) + [int(coef)], variable)


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
