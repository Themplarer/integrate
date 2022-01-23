import re

from polynomials.integer_polynomial import IntegerPolynomial

_monom_regexp = re.compile(
    r'\(?((?P<coef>-?\d+)*\)?(\*?\(?(?P<var>[A-Za-z])\)?(('
    r'?P<powersymbol>\^|\*\*)'
    r'(?P<power>\d*)\)?)?)?)')


def parse(poly, variable='x'):
    all_letters = set(filter(lambda l: l.isalpha(), poly))
    if any(all_letters.difference(variable)):
        raise ValueError('can only parse a polynomial with one variable: '
                         f'{variable}')

    if variable not in all_letters:
        return IntegerPolynomial((eval(poly),), variable)

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
        elif brackets_balance == 0 and symbol in {'*', '/'} and \
                poly[index - 1] != '*' and poly[index + 1] != '*':
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
