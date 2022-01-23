class RationalFunction:
    def __init__(self, numerator_poly, denominator_poly=1, poly_part=0):
        if not denominator_poly:
            raise ZeroDivisionError('denominator must not be equal to 0')

        self.denominator = denominator_poly
        self.poly_part, self.numerator = divmod(numerator_poly,
                                                denominator_poly)
        if poly_part:
            self.poly_part += poly_part

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
                (self.poly_part * self.denominator + self.numerator) *
                other.denominator,
                (other.poly_part * other.denominator + other.numerator) *
                self.denominator)

        return RationalFunction(
            (self.poly_part * self.denominator + self.numerator),
            self.denominator * other)

    def __str__(self):
        s = ''
        if self.poly_part:
            s = self.poly_part + ' + '

        return s + f'({self.numerator})/({self.denominator})'
