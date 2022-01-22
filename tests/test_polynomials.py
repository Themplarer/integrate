import unittest
from fractions import Fraction

from polynomials.integer_polynomial import IntegerPolynomial
from polynomials.polynomial import Polynomial


class TestPolynomials(unittest.TestCase):
    def test_init_zero(self):
        p = Polynomial([0])
        # да, обычно считается, что нулевой многочлен имеет степень -inf,
        # но нам это не нужно (и даже немного мешает)
        self._assert_polynomials_equal(p, (0,), 0, '0')

    def test_constant(self):
        p = Polynomial([1])
        self._assert_polynomials_equal(p, (1,), 0, '1')

    def test_removes_redundant_zero_coeffs(self):
        p = Polynomial([1, 2, 3, 0, 0, 0])
        self._assert_polynomials_equal(p, (1, 2, 3), 2, '3x^2+2x+1')

    def test_works_right_with_zeroes_inside(self):
        p = Polynomial([1, 0, 3, 4])
        self._assert_polynomials_equal(p, (1, 0, 3, 4), 3, '4x^3+3x^2+1')

    def test_neg_coeffs(self):
        p = Polynomial([1, 0, -3, -4])
        self._assert_polynomials_equal(p, (1, 0, -3, -4), 3, '-4x^3-3x^2+1')

    def test_coeffs_with_magnitude_1(self):
        p = Polynomial([1, 0, -1, 1])
        self._assert_polynomials_equal(p, (1, 0, -1, 1), 3, 'x^3-x^2+1')

    def test_add_polynomials(self):
        p1 = Polynomial([1, 0, -1, 1])
        p2 = Polynomial([1, 0, 3, 4])
        self.assertTupleEqual((2, 0, 2, 5), (p1 + p2).coeffs)

    def test_add_with_different_vars(self):
        p1 = Polynomial([1, 0, -1, 1])
        p2 = Polynomial([1, 0, 3, 4], 'y')
        with self.assertRaises(ValueError) as e:
            p1 + p2

        self.assertEqual(e.exception.args[0], 'impossible to add two '
                                              'polynomials with different '
                                              'variables!')

    def test_add_with_not_a_pol(self):
        p1 = Polynomial([1, 0, -1, 1])
        with self.assertRaises(ValueError) as e:
            p1 + 'test'

        self.assertEqual(e.exception.args[0],
                         'impossible to add polynomial and str!')

    def test_sub_polynomials(self):
        p1 = Polynomial([1, 0, -1, 1])
        p2 = Polynomial([1, 0, 3, 1])
        self.assertTupleEqual((0, 0, -4), (p1 - p2).coeffs)

    def test_sub_with_different_vars(self):
        p1 = Polynomial([1, 0, -1, 1])
        p2 = Polynomial([1, 0, 3, 4], 'y')
        with self.assertRaises(ValueError) as e:
            p1 - p2

        self.assertEqual(e.exception.args[0], 'impossible to subtract two '
                                              'polynomials with different '
                                              'variables!')

    def test_sub_with_not_a_pol(self):
        p1 = Polynomial([1, 0, -1, 1])
        with self.assertRaises(ValueError) as e:
            p1 - 'test'

        self.assertEqual(e.exception.args[0],
                         'impossible to subtract polynomial and str!')

    def test_mul_polynomials1(self):
        p1 = Polynomial([1, 2])
        p2 = Polynomial([3, 1])
        self.assertTupleEqual((3, 7, 2), (p1 * p2).coeffs)

    def test_mul_polynomials2(self):
        p1 = Polynomial([1, 1])
        p2 = Polynomial([1, 1])
        self.assertTupleEqual((1, 2, 1), (p1 * p2).coeffs)

    def test_mul_with_different_vars(self):
        p1 = Polynomial([1, 0, -1, 1])
        p2 = Polynomial([1, 0, 3, 4], 'y')
        with self.assertRaises(ValueError) as e:
            p1 * p2

        self.assertEqual(e.exception.args[0], 'impossible to multiply '
                                              'two polynomials with '
                                              'different variables!')

    def test_mul_with_not_a_pol(self):
        p1 = Polynomial([1, 0, -1, 1])
        with self.assertRaises(ValueError) as e:
            p1 * 'test'

        self.assertEqual(e.exception.args[0],
                         'impossible to multiply polynomial and str!')

    def test_neg_polynomials1(self):
        p1 = Polynomial([1, 2])
        self.assertTupleEqual((-1, -2), (-p1).coeffs)

    def test_eq_polynomials_with_different_vars(self):
        p1 = Polynomial([1, 0, -1, 1])
        p2 = Polynomial([1, 0, -1, 1], 'y')
        self.assertEqual(p1, p2)

    def test_eq_polynomials_with_almost_same_coeffs(self):
        p1 = Polynomial([1, 0, -1, 1])
        p2 = Polynomial([1, -1, 0, 1])
        self.assertNotEqual(p1, p2)

    def test_eq_polynomials_with_not_a_pol(self):
        p1 = Polynomial([1, 0, -1, 1])
        self.assertNotEqual(p1, '1')

    def test_add_int_to_int_poly(self):
        p1 = IntegerPolynomial([1, 0, -1, 1])
        self.assertTupleEqual((2, 0, -1, 1), (p1 + 1).coeffs)

    def test_sub_int_from_int_poly(self):
        p1 = IntegerPolynomial([1, 0, -1, 1])
        self.assertTupleEqual((0, 0, -1, 1), (p1 - 1).coeffs)

    def test_add_rational_to_rational_poly(self):
        p1 = IntegerPolynomial([1, 0, -1, 1])
        self.assertTupleEqual((Fraction(3, 2), 0, -1, 1),
                              (p1 + Fraction(1, 2)).coeffs)

    def test_sub_rational_from_int_poly(self):
        p1 = IntegerPolynomial([1, 0, -1, 1])
        self.assertTupleEqual((Fraction(1, 2), 0, -1, 1),
                              (p1 - Fraction(1, 2)).coeffs)

    def _assert_polynomials_equal(self, polynomial, coeffs, power, str_repr):
        self.assertTupleEqual(coeffs, polynomial.coeffs)
        self.assertEqual(power, polynomial.power)
        self.assertEqual(str_repr, str(polynomial))


if __name__ == '__main__':
    unittest.main()
