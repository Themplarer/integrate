from fractions import Fraction

from polynomials.polynomial import Polynomial
from rationalfunction import RationalFunction


class Function:
    def __init__(self, terms):
        self.terms = terms

    def __str__(self):
        strings = []
        is_first = True
        for i, j in self.terms.items():
            if not j:
                continue

            if not is_first:
                strings.append('+')

            is_first = False
            if j != 1:
                n = str(j)
                if j < 0:
                    n = '(' + n + ')'

                strings.append(n)

            if j != 1:
                strings.append('(')

            strings.append(str(i))

            if j != 1:
                strings.append(')')

        return ''.join(strings)


def integrate_polynomial(p):
    coeffs = [0] + [Fraction(j) / (i + 1) for i, j in enumerate(p.coeffs)]
    return Polynomial(coeffs, p.variable)


def integrate_rational_func(r):
    subfuncs = dict()
    if isinstance(r, Polynomial):
        subfuncs[integrate_polynomial(r)] = 1

    if isinstance(r, RationalFunction):
        subfuncs[integrate_polynomial(r.poly_part)] = 1

        if r.denominator.power == 1:
            subfuncs[f'ln({r.denominator})'] = r.numerator / r.denominator[-1]
        elif r.denominator.power == 2:
            e, d, c = r.denominator
            num = r.numerator

            if num.power == 1:
                b, a = r.numerator

                subfuncs[f'ln({r.denominator / c})'] = a / (2 * c)
                num = Polynomial(((2 * b * c - a * d) / (2 * c),), num.variable)

            if num.power == 0:
                discriminant = d ** 2 - 4 * c * e
                if discriminant == 0:
                    subfuncs[f'1/({num.variable}+-[] nvb234byrdtfnki;"hkjly ' \
                             f'qrwerty'] = a /\
                                                                          (2 * c)


        else:
            raise ValueError("polynomials' degrees are too high: can't "
                             "integrate")

    subfuncs['C'] = 1
    return Function(subfuncs)
