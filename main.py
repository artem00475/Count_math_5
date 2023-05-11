import sys

from console_utils import print_to_output, enter_value, get_interval, get_x
from file_utils import print_to_file
import matplotlib.pyplot as plt
import numpy as np

from func_utils import func
from interpolation import count_finite_differences, lagranzhe_method, newton_method, stirling_method, bessel_method


# Преобразование уравнения в обратную польскую запись
def to_pol_format(st):
    a = st.split()
    res = []
    op = []
    symb = {'-': 0, '+': 0, '*': 1, '^': 2, 'cos': 3, 'sin': 3}
    for s in a:
        if s not in symb:
            if s != "x" and s != "x_1" and s != "x_2":
                res.append(float(s))
            else:
                res.append(s)
        else:
            if len(op) == 0:
                op.append(s)
            else:
                sm = op.pop()
                if symb[s] <= symb[sm]:
                    res.append(sm)
                    while len(op) > 0 and symb[s] <= symb[op[-1]]:
                        sm = op.pop()
                        res.append(sm)
                else:
                    op.append(sm)
                op.append(s)
    while len(op) > 0:
        res.append(op.pop())
    return res


# Считывание размерности матрицы
def get_matrix_size():
    # Ввод с клавиатуры
    while True:
        print("Введите целое число - количесвто точек в таблице:")
        try:
            size_string = input()
            size = int(size_string)
            return size
        except ValueError:
            print("Некорректное значение. Повторите ввод.")
            continue


# Считывание элементов матрицы
def get_matrix_values(size):
    # Ввод с клавиатуры
    while True:
        table = [['   x   ', '   y   ']]
        for row in range(size):
            while True:
                print("Введите координаты ", row + 1, " точки через пробел:")
                try:
                    elements_string = input().split()
                    if len(elements_string) != 2:
                        print("Неправильное количество элементов в строке")
                        continue
                    table.append(list(map(float, elements_string)))
                    break
                except ValueError:
                    print("Некорректные значения. Повторите ввод.")
                    continue
        return table


def get_matrix_from_file():
    while True:
        print("Выберите файл:")
        print("1. 1.txt")
        print("2. 2.txt")
        print("3. 3.txt")
        print("4. Свой файл")
        file_num = enter_value(1, 4)
        if file_num == 1:
            file = "1.txt"
        elif file_num == 2:
            file = "2.txt"
        elif file_num == 3:
            file = "3.txt"
        else:
            print(
                "Данные в файле должны быть в формате каждая пара в отдельной строке файла, элементы в строке разделяются пробелами. В первой строке количесвто точек")
            file = input("Введите имя файла: ")
        try:
            file = open(file, 'r')
            matrix_size = int(file.readline())
            if matrix_size < 2:
                print("Число точек должно быть больше 2")
                continue
            table = [['   x   ', '   y   ']]
            for row in range(matrix_size):
                elements_string = file.readline().split()
                if len(elements_string) != 2:
                    print("Неправильное количество элементов в строке", row + 1)
                    raise ArithmeticError
                table.append(list(map(float, elements_string)))
            return matrix_size, table
        except FileNotFoundError:
            print("Файл не найден. Попробуйте еще раз.")
            continue
        except ValueError:
            print("Некорректное значение. Повторите ввод.")
            continue
        except ArithmeticError:
            continue


# Вывод результата
def print_result(x, y, p, e, dev, s, k, table, c, num):
    text = ["Наилучшее приближение - линейное", "Наилучшее приближение - квадратичное",
            "Наилучшее приближение - полином 3 степени", "Наилучшее приближение - степенное",
            "Наилучшее приближение - экспоненциальное", "Наилучшее приближение - логарифмическое"]
    while True:
        t = input("Для вывода в консоль введите c, для сохранения в файл введите f: ")
        if t.split()[0] == "f":
            print_to_file(x, y, p, e, dev, s, k, table, c, text[num])
            break
        elif t.split()[0] == "c":
            print_to_output(x, y, p, e, dev, s, k, table, c, text[num])
            break
        else:
            print("Повторите ввод")


def print_table(table):
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


print("Интерполяция фукнции.")
print("Выберите способ задания исходных данных:")
print("1. Ввести с клавиатуры")
print("2. Ввести из файла")
print("3. Выбрать функцию")
inputed = enter_value(1, 3)
if inputed == 1:
    matrix_size = get_matrix_size()
    table = get_matrix_values(matrix_size)
elif inputed == 2:
    matrix_size, table = get_matrix_from_file()
else:
    f = open("equations.txt")
    count = int(f.readline())
    print("Выбирите подинтегральную функцию:")
    equations = []
    equation = False
    try:
        for x in range(1, count + 1):
            e = f.readline().replace('\n', '')
            s = str(x) + '. ' + e
            equations.append(to_pol_format(e))
            print(s)
        number = enter_value(1, count)
        equation = equations[number - 1]
    except ValueError:
        print("Ошибка в введенном уравнении")
    if equation:
        a, b = get_interval()
        print("Введите кол-во точек: ")
        matrix_size = enter_value(b, sys.maxsize)
        h = (b-a)/matrix_size
        table = [['   x   ', '   y   ']]
        for i in range(matrix_size):
            table.append([a + i * h, func(equation, a+i*h)])
print("Количество точек - ", matrix_size)
print("\nВведенная таблица")
print_table(table)
print()

x_table = []
y_table = []
for i in range(1, len(table)):
    x_table.append(table[i][0])
    y_table.append(table[i][1])
finite_differences = count_finite_differences(x_table, y_table, matrix_size)
print_table(finite_differences)
x = get_x(min(x_table), max(x_table))
print(x)

lagranzh = lagranzhe_method(x_table, y_table, matrix_size, x, True)
newton = newton_method(x_table, y_table, matrix_size, x, finite_differences, True, 0)
stirling = stirling_method(x_table, y_table, matrix_size, x, finite_differences, True)
bessel = bessel_method(x_table, y_table, matrix_size, x, finite_differences, True)
num = 0
for i in range(len(x_table)):
    if x_table[i] > x:
        num = i-1
        break
y0 = y_table[num]
y1 = y_table[num+1]

if y0 <= lagranzh <= y1:
    print("Значения в методе Лагранжа попало в интервал.")
else:
    print("Значения в методе Лагранжа не попало в интервал.")
if y0 <= newton[0] <= y1:
    print("Значения в методе Ньютона попало в интервал.")
else:
    print("Значения в методе Ньютона не попало в интервал.")
if bessel[1]:
    if y0 <= bessel[0] <= y1:
        print("Значения в методе Бесселя попало в интервал.")
    else:
        print("Значения в методе Бесселя не попало в интервал.")
if stirling[1]:
    if y0 <= stirling[0] <= y1:
        print("Значения в методе Стирлинга попало в интервал.")
    else:
        print("Значения в методе Стирлинга не попало в интервал.")
print("Отлонение между Лагранжом и Ньютоном:", abs(lagranzh-newton[0]))
if bessel[1]:
    print("Отлонение между Лагранжом и Бесселем:", abs(lagranzh - bessel[0]))
    print("Отлонение между Ньютоном и Бесселем:", abs(newton[0] - bessel[0]))
if stirling[1]:
    print("Отлонение между Лагранжом и Стирлингом:", abs(lagranzh - stirling[0]))
    print("Отлонение между Ньютоном и Стирлингом:", abs(newton[0] - stirling[0]))


l_table = []
n_table = []
s_table = []
b_table = []
x = np.arange(float(min(x_table)), float(max(x_table)) + 0.01, 0.01)
for i in x:
    l_table.append(lagranzhe_method(x_table, y_table, matrix_size, i, False))
    n_table.append(newton_method(x_table, y_table, matrix_size, i, finite_differences, False, newton[1])[0])
    if stirling[1]:
        s_table.append(stirling_method(x_table, y_table, matrix_size, i, finite_differences, False)[0])
    if bessel[1]:
        b_table.append(bessel_method(x_table, y_table, matrix_size, i, finite_differences, False)[0])
if inputed == 3:
    plt.scatter(x_table, y_table)
    c_table = []
    for i in x:
        c_table.append(func(equation, i))
    plt.plot(x, c_table, label='Исходная функция')
else:
    plt.plot(x_table, y_table, label='Исходная функция', marker='o')
plt.plot(x, l_table, label='Многочлен Лагранжа')
plt.plot(x, n_table, label='Многочлен Ньютона')
if stirling[1]:
    plt.plot(x, s_table, label='Многочлен Стирлинга')
if bessel[1]:
    plt.plot(x, b_table, label='Многочлен Бесселя')

plt.grid(True)
plt.legend()
plt.show()
