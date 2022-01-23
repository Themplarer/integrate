import argparse

from integrator import integrate_rational_func
from parse import parse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', default='x',
                        help='Переменная интегрирования. По умолчанию - x')
    parser.add_argument('func',
                        help='Рациональная функция (отношение многочленов с '
                             'целыми коэффициентами от данной переменной). '
                             'Может содержать пробелы (однако, для этого '
                             'нужно заключить выражение в кавычки). '
                             'Поддерживается использование ** и ^ для '
                             'обозначения возведения в степень. '
                             'Пример функции - '
                             '2x^2+5x**3 + (-8)x * x^2')

    args = parser.parse_args()
    try:
        print(integrate_rational_func(
            parse(args.func.replace(' ', ''), args.v)))
    except (AttributeError, ValueError, ZeroDivisionError) as e:
        print(e)


if __name__ == '__main__':
    main()
