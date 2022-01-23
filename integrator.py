from fractions import Fraction

from polynomials.rational_polynomial import RationalPolynomial


class Function:
    def __init__(self, terms):
        self.terms = terms

    def __str__(self):
        strings = []
        is_first = True
        for i, j in self.terms.items():
            if not j:
                continue

            s = str(i)
            if not is_first:
                strings.append('+')

            is_first = False
            strings.append('(')
            strings.append(j)
            strings.append(')')
            strings.append('(')
            strings.append(s)
            strings.append(')')

        return ''.join(strings)


def integrate_polynomial(p):
    coeffs = [0] + [Fraction(j) / (i + 1) for i, j in enumerate(p.coeffs)]
    return RationalPolynomial(coeffs, p.variable)


def integrate_rational_func(r):
    poly_func_integrated = integrate_polynomial(r.poly_part)

    return Function({poly_func_integrated: 1})
