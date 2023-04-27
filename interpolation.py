def count_finite_differences(x_table, y_table, size):
    table = [['№', '   x_i   ', '  y_i   ']]
    for i in range(3, size+2):
        table[0].append(' ∆^'+str(i-2)+'y_i ')
    for i in range(size):
        table.append([i, x_table[i], y_table[i]])
    a = size - 1
    while a > 0:
        for i in range(a):
            table[i+1].append(table[i + 2][-1] - table[i+1][-1])
        a -= 1
    return table


def lagranzhe_method(x_table, y_table, size, x, printed):
    if printed:
        print("Интерполяция методом Лагранжа.")
    l = 0
    for i in range(size):
        p = y_table[i]
        for j in range(size):
            if j == i:
                continue
            p *= (x-x_table[j])/(x_table[i]-x_table[j])
        l += p
    if printed:
        print("L_"+str(size-1)+"(x) = "+str(round(l, 5)))
    return l


def newton_method(x_table, y_table, size, x, finite_differences, printed):
    if len(x_table) % 2 == 0:
        middle = x_table[len(x_table) // 2 - 1]
    else:
        middle = x_table[len(x_table)//2]
    if x > middle:
        if printed:
            print("Интерполяция по второй формуле Ньютона.")
        h = x_table[1] - x_table[0]
        t = (x - x_table[-1])/h
        n = y_table[-1]
        for i in range(size-1):
            p = finite_differences[size-i-1][i+3]
            for j in range(1, i+2):
                p *= (t+j-1)/j
            n += p
        if printed:
            print("P_" + str(size - 1) + "(x) = " + str(round(n, 5)))
        return n
    else:
        if printed:
            print("Интерполяция по первой формуле Ньютона.")
        h = x_table[1] - x_table[0]
        t = (x - x_table[0]) / h
        n = y_table[0]
        for i in range(size-1):
            p = finite_differences[1][i + 3]
            for j in range(1, i + 2):
                p *= (t - j + 1) / j
            n += p
        if printed:
            print("P_" + str(size - 1) + "(x) = " + str(round(n, 5)))
        return n


def stirling_method(x_table, y_table, size, x, finite_differences, printed):
    if len(x_table) % 2 == 0:
        if printed:
            print("Интерполяция методом Стирлинга невозможна. Четное количество узлов")
        return [0, False]
    middle = (len(x_table) + 1) // 2
    h = x_table[1] - x_table[0]
    t = (x-x_table[middle-1])/h
    if abs(t) > 0.25:
        if printed:
            print("Интерполяция методом Стирлинга невозможна. t слишком велико")
        return [0, False]
    if printed:
        print("Интерполяция методом Стирлинга")
    s = y_table[middle-1]
    for i in range(1, (size+1)//2):
        pow = 2*i-1
        p = 1
        for j in range(1, i):
            p *= (t**2-j**2)
        p1 = (p * t * (finite_differences[middle-i][2+pow]+finite_differences[middle+1-i][2+pow]))/(2 * faq(pow))
        p2 = (finite_differences[middle-i][3+pow]*t**2 * p)/faq(2*i)
        s += p1 + p2
    if printed:
        print("S_" + str(size - 1) + "(x) = " + str(round(s, 5)))
    return [s, True]


def faq(n):
    s = 1
    for i in range(1, n+1):
        s *= i
    return s


def bessel_method(x_table, y_table, size, x, finite_differences, printed):
    if len(x_table) % 2 == 1:
        if printed:
            print("Интерполяция методом Бесселя невозможна. Нечетное количество узлов")
        return [0, False]
    middle = (len(x_table)) // 2 - 1
    h = x_table[1] - x_table[0]
    t = (x-x_table[middle])/h
    if abs(t) < 0.25 or abs(t) > 0.75:
        if printed:
            print("Интерполяция методом Бесселя невозможна. t выходит за пределы диапозона")
        return [0, False]
    if printed:
        print("Интерполяция методом Бесселя")
    b = (y_table[middle] + y_table[middle+1])/2 + (t-0.5)*finite_differences[middle+1][3]
    for i in range(1, size//2):
        pow = 2*i
        p = 1
        for j in range(i):
            p *= (t-j)*(t+j-1)
        p1 = (p * (finite_differences[middle+1-i][2+pow]+finite_differences[middle+2-i][2+pow]))/(2*faq(pow))
        p2 = (finite_differences[middle+1-i][3+pow]*(t-0.5)*p)/faq(2*i+1)
        b += p1 + p2
    if printed:
        print("B_" + str(size - 1) + "(x) = " + str(round(b, 5)))
    return [b, True]
