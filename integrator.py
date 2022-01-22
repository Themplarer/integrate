from fractions import Fraction

from polynomials.rational_polynomial import RationalPolynomial


def integrate_polynomial(p):
    coeffs = [0] + [Fraction(j) / (i + 1) for i, j in enumerate(p.coeffs)]
    return RationalPolynomial(coeffs, p.variable)
