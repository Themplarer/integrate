class Function:
    def __init__(self, terms):
        self.terms = terms

    def __str__(self):
        strings = []
        is_first = True
        for i, j in self.terms.items():
            if not i or not j:
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
