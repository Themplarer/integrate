import itertools as it


class Polynomial:
    """Описывает многочлен над некоторым полем со сложением и умножением"""

    def __init__(self, coeffs_by_powers_desc, variable='x'):
        end = len(coeffs_by_powers_desc)
        for c in reversed(coeffs_by_powers_desc):
            if c:
                break
            end -= 1

        self.coeffs = tuple(coeffs_by_powers_desc[:max(1, end)])
        self.variable = variable

    def __add__(self, other):
        return self._add_signed(other, True)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self._add_signed(other, False)

    def __rsub__(self, other):
        return -self + other

    def __mul__(self, other):
        if isinstance(other, int):
            return Polynomial([other * i for i in self.coeffs], self.variable)

        if isinstance(other, Polynomial):
            if self.variable != other.variable:
                raise ValueError('impossible to multiply two polynomials with '
                                 'different variables!')

            coeffs = list()
            for i in range(self.power + other.power + 1):
                coeff = 0
                for j in range(max(0, i - other.power), min(i, self.power) + 1):
                    coeff += self.coeffs[j] * other.coeffs[i - j]

                coeffs.append(coeff)

            return Polynomial(coeffs, self.variable)

        raise ValueError('impossible to multiply polynomial and '
                         f'{type(other).__name__}!')

    def __divmod__(self, other):
        if isinstance(other, Polynomial):
            if self.variable != other.variable:
                raise ValueError('impossible to divide two polynomials with '
                                 'different variables!')

            o = self
            res = Polynomial([0], self.variable)

            while o.power >= other.power:
                div = Polynomial([0] * (o.power - other.power) +
                                 [o.coeffs[-1] / other.coeffs[-1]])
                res += div
                o -= div * other

            return res, o

        raise ValueError('impossible to divide polynomial and '
                         f'{type(other).__name__}!')

    def __rmul__(self, other):
        return self * other

    def __neg__(self):
        return self * (-1)

    def __eq__(self, other):
        return isinstance(other, Polynomial) and self.coeffs == other.coeffs

    def __str__(self):
        def monom_to_str(power, coef):
            if not power:
                return str(coef)

            strs = [self.variable]
            if coef == -1:
                strs.insert(0, '-')
            elif coef != 1:
                strs.insert(0, str(coef))

            if power != 1:
                strs.append('^')
                strs.append(str(power))

            return ''.join(strs)

        if self.power == 0:
            return str(self.coeffs[0])

        strings = []
        is_first = True
        for i, j in reversed(list(enumerate(self.coeffs))):
            if not j:
                continue

            s = monom_to_str(i, j)
            if not is_first and (isinstance(j, str) or j > 0):
                strings.append('+')

            is_first = False
            strings.append(s)

        return ''.join(strings)

    @property
    def power(self):
        return len(self.coeffs) - 1

    def _add_signed(self, other, is_adding):
        verb = 'add' if is_adding else 'subtract'
        func = (lambda x: x[0] + x[1]) if is_adding else \
            (lambda x: x[0] - x[1])

        if isinstance(other, Polynomial):
            if self.variable != other.variable:
                raise ValueError(f'impossible to {verb} two polynomials with '
                                 'different variables!')

            new_coeffs = it.zip_longest(self.coeffs, other.coeffs, fillvalue=0)
            return Polynomial([*(map(func, new_coeffs))], self.variable)

        raise ValueError(f'impossible to {verb} polynomial and '
                         f'{type(other).__name__}!')
