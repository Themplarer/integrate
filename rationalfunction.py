import re

from polynomials.integer_polynomial import IntegerPolynomial

_monom_regexp = re.compile(
    r'((?P<coef>-?\d+)*(\*?(?P<var>[A-Za-z])((?P<powersymbol>\^|\*\*)'
    r'(?P<power>\d*))?)?)')


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
        elif brackets_balance == 0 and symbol in {'*', '/'}:
            left = parse(poly[:index], variable)
            right = parse(poly[index + 1:], variable)
            return left * right if symbol == '*' else left / right

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


class RationalFunction:
    def __init__(self, numerator_poly, denominator_poly=1, poly_part=0):
        if not denominator_poly:
            raise ZeroDivisionError('denominator must not be equal to 0')

        self.poly_part, self.numerator = divmod(numerator_poly,
                                                denominator_poly)
        self.poly_part += poly_part
        self.denominator = denominator_poly

        divisor = self.denominator / self.numerator
        self.numerator /= divisor
        self.denominator /= divisor

    def __add__(self, other):
        if isinstance(other, RationalFunction):
            return RationalFunction(self.numerator * other.denominator +
                                    self.denominator * other.numerator,
                                    self.denominator * other.denominator,
                                    self.poly_part + other.poly_part)

        return RationalFunction(self.numerator, self.denominator,
                                self.poly_part + other)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + (-1) * other

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        if isinstance(other, RationalFunction):
            return RationalFunction(
                self.poly_part * self.denominator * other.numerator +
                self.numerator * other.poly_part * other.denominator +
                self.numerator * other.numerator,
                self.denominator * other.denominator,
                self.poly_part * other.poly_part)

        return RationalFunction(self.numerator * other, self.denominator,
                                self.poly_part * other)

    def __rmul__(self, other):
        return self * other

    def __neg__(self):
        return (-1) * self

    def __truediv__(self, other):
        if isinstance(other, RationalFunction):
            return RationalFunction(
                (
                        self.poly_part * self.denominator + self.numerator) * other.denominator,
                (other.poly_part * other.denominator +
                 other.numerator) * self.denominator)
