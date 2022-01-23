from fractions import Fraction
from math import sqrt

from function import Function
from polynomials.polynomial import Polynomial
from polynomials.rational_polynomial import RationalPolynomial
from rational_function import RationalFunction


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
            _integrate_and_add_res_denominator_second_pow(r, subfuncs)
        else:
            raise ValueError("polynomials' degrees are too high: can't "
                             "integrate")

    subfuncs['C'] = 1
    return Function(subfuncs)


def _integrate_and_add_res_denominator_second_pow(r, subfuncs):
    e, d, c = r.denominator.coeffs
    num = r.numerator
    v = r.numerator.variable

    if num.power == 1:
        b, a = num.coeffs

        subfuncs[f'ln({r.denominator / c})'] = a / (2 * c)
        num = Polynomial(((2 * b * c - a * d) / (2 * c),), v)

    if num.power == 0:
        discriminant = d ** 2 - 4 * c * e
        if discriminant == 0:
            root = Fraction(-d, (2 * c))
            f = RationalFunction(1, RationalPolynomial((-root, 1), v))
            subfuncs[f] = Fraction(num.coeffs[-1], c)
        elif discriminant < 0:
            x = 2 * c / (Fraction(sqrt(-discriminant)))
            p = RationalPolynomial((d / 2, 1), v) * x
            subfuncs[f'arctg({p})'] = x * num.coeffs[-1] / c
        else:
            x = Fraction(sqrt(discriminant))
            root1, root2 = (-d - x) / (2 * c), (-d + x) / (2 * c)

            f1 = 1 / RationalPolynomial((-root1, 1), v)
            subfuncs[f'ln({f1})'] = Fraction(num.coeffs[-1], x)

            f2 = 1 / RationalPolynomial((-root2, 1), v)
            subfuncs[f'ln({f2})'] = -Fraction(num.coeffs[-1], x)
