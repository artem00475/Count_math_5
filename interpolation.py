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
    middle = x_table[len(x_table)//2+1]
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
