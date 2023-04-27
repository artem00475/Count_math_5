import sys

from aproximation import linear, quadratic, third, power, exponential, logarithmic
from console_utils import print_to_output, enter_value, get_interval, get_x
from file_utils import print_to_file
import matplotlib.pyplot as plt
import numpy as np

from func_utils import func
from interpolation import count_finite_differences, lagranzhe_method, newton_method


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

lagranzh = lagranzhe_method(x_table, y_table, matrix_size, x)
newton = newton_method(x_table, y_table, matrix_size, x, finite_differences)

res = [[' X   ']]
for i in range(matrix_size):
    res.append([round(float(x_table[i]), 4)])
res.append([' δ '])
# линейная
p_table_l, e_table_l, deviation_l, s_l, a_l, b_l, cor = linear(matrix_size, x_table, y_table)
res[0].append('  Y_л   ')
# квадратичная
p_table_q, e_table_q, deviation_q, s_q, k_q = quadratic(matrix_size, x_table, y_table)
res[0].append('  Y_к   ')
# 3 степень
p_table_3, e_table_3, deviation_3, s_3, k_3 = third(matrix_size, x_table, y_table)
res[0].append('  Y_3   ')
for i in range(matrix_size):
    res[i + 1].append(round(float(p_table_l[i]), 5))
    res[i + 1].append(round(float(p_table_q[i]), 5))
    res[i + 1].append(round(float(p_table_3[i]), 5))
res[-1] += [round(deviation_l, 5), round(deviation_q, 5), round(deviation_3, 5)]

deviation_s = 10 ** 6
deviation_e = 10 ** 6
deviation_log = 10 ** 6
expon = False
log = False
if float(min(x_table)) > 0 and float(min(y_table)) > 0:
    # степенная
    p_table_s, e_table_s, deviation_s, s_s, a_s, b_s = power(matrix_size, x_table, y_table)
    res[0].append('  Y_с   ')
    for i in range(matrix_size):
        res[i + 1].append(round(float(p_table_s[i]), 5))
    res[-1].append(round(deviation_s, 5))
else:
    print("Аппроксимация степенной функцией невозможна")
if float(min(y_table)) > 0:
    res[0].append('  Y_э   ')
    # экспоненциальная
    p_table_e, e_table_e, deviation_e, s_e, a_e, b_e = exponential(matrix_size, x_table, y_table)
    for i in range(matrix_size):
        res[i + 1].append(round(float(p_table_e[i]), 5))
    res[-1].append(round(deviation_e, 5))
else:
    print("Аппроксимация экспоненциальной функцией невозможна")
if float(min(x_table)) > 0:
    res[0].append(' Y_лог ')
    # логарифмическая
    p_table_log, e_table_log, deviation_log, s_log, a_log, b_log = logarithmic(matrix_size, x_table, y_table)
    for i in range(matrix_size):
        res[i + 1].append(round(float(p_table_log[i]), 5))
    res[-1].append(round(deviation_log, 5))
else:
    print("Аппроксимация логарифмической функцией невозможна")

dev = [deviation_l, deviation_q, deviation_3, deviation_s, deviation_e, deviation_log]
num = dev.index(min(dev))
if num == 0:
    print_result(x_table, y_table, p_table_l, e_table_l, deviation_l, s_l, [a_l, b_l], res, cor, 0)
elif num == 1:
    print_result(x_table, y_table, p_table_q, e_table_q, deviation_q, s_q, k_q, res, cor, 1)
elif num == 2:
    print_result(x_table, y_table, p_table_3, e_table_3, deviation_3, s_3, k_3, res, cor, 2)
elif num == 3:
    print_result(x_table, y_table, p_table_s, e_table_s, deviation_s, s_s, [a_s, b_s], res, cor, 3)
elif num == 4:
    print_result(x_table, y_table, p_table_e, e_table_e, deviation_e, s_e, [a_e, b_e], res, cor, 4)
elif num == 5:
    print_result(x_table, y_table, p_table_log, e_table_log, deviation_log, s_log, [a_log, b_log], res, cor, 5)

x = np.arange(float(min(x_table)) - 0.5, float(max(x_table)) + 0.51, 0.01)
plt.plot(x_table, y_table, label='Исходная функция')
plt.plot(x, a_l * x + b_l, label='Линейное приближение')
plt.plot(x, k_q[0] + k_q[1] * x + k_q[2] * x ** 2, label='Квадратичное приближение')
plt.plot(x, k_3[0] + k_3[1] * x + k_3[2] * x ** 2 + k_3[3] * x ** 3, label='Полином 3 степени')
if float(min(x_table)) > 0 and float(min(y_table)) > 0:
    plt.plot(x, a_s * x ** b_s, label='Степенное приближение')
if float(min(y_table)) > 0:
    plt.plot(x, a_e * np.exp(b_e * x), label='Экспоненциальное приближение')
if float(min(x_table)) > 0:
    plt.plot(x, a_log * np.log(x) + b_log, label='Логарифмическое приближение')
plt.grid(True)
plt.legend()
plt.show()
