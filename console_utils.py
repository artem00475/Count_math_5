# Считывание числа с клавиатуры
def enter_value(b, c):
    a = 0
    while a < b or a > c:
        try:
            a = int(input())
            if a < b or a > c:
                raise ValueError
        except ValueError:
            print("Повторите ввод")
    return a


# Считывание интервала для нахождения корня с клавиатуры
def get_interval():
    # while True:
    print("Введите левую границу интервала")
    flaga = False
    a = 0
    while not flaga:
        try:
            a = float(input())
            flaga = True
        except ValueError:
            print("Повторите ввод")
    print("Введите правую границу интервала")
    flagb = False
    b = 0
    while not flagb:
        try:
            b = float(input())
            if b == a:
                raise ValueError
            flagb = True
        except ValueError:
            print("Повторите ввод")
    return min(a, b), max(a, b)


def get_x(a, b):
    print("Введите точку, в которой нужно найти значение функции:")
    flagс = False
    d = 0
    while not flagс:
        try:
            d = float(input())
            if d >= b or d <= a:
                print("Точка должна быть внутри интервала")
                continue
            flagс = True
            return d
        except ValueError:
            print("Повторите ввод")


def print_table(x, y, p, e):
    b = [x, y, p, e]
    a = [' x  ', ' y  ', 'P(x)', ' e  ']
    for i in range(4):
        print(a[i], end=' ')
        for c in b[i]:
            print('%.5f' % c, end=' ')
        print()


def print_table_res(table):
    for c in table[0]:
        print(c, end='    ')
    print()
    for row in table[1:]:
        count = 0
        for c in row:
            if count == 0:
                print(c, end='    ')
                count += 1
            else:
                if c >= 0:
                    print(' %.5f' % c, end='    ')
                else:
                    print('%.5f' % c, end='    ')
        print()


# Вывод результата в поток вывода
def print_to_output(x, y, p, e, dev, s, k, table, cor, text):
    print("Результаты аппрокссимации:")
    print_table_res(table)
    print("Коэффициент корреляции Пирсона:", round(cor, 6), '\n')
    print(text)
    print("Среднеквадратичное отклонение:", round(dev, 6))
    print("Мера отклонения:", round(s, 6))
    if len(k) == 2:
        print("Коэффиценты апроксимирующей фукнции: a =", k[0], "b =", k[1])
    elif len(k) == 3:
        print("Коэффиценты апроксимирующей фукнции: a =", k[2], "b =", k[1], "c =", k[0])
    else:
        print("Коэффиценты апроксимирующей фукнции: a =", k[3], "b =", k[2], "c =", k[1], "d =", k[0])
    print_table(x, y, p, e)
