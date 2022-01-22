import argparse

from integrator import integrate_polynomial
from polynomials.integer_polynomial import parse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', default='x', help='')
    parser.add_argument('polynomial', help='')

    args = parser.parse_args()
    # try:
    print(integrate_polynomial(
            parse(args.polynomial.replace(' ', ''), args.v)))
    # except (AttributeError, ValueError, ZeroDivisionError) as e:
    #     print(e)


if __name__ == '__main__':
    main()
