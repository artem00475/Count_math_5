import numpy as np


# Вычисление значение функции
def func(eq, x):
    s = []
    symb = {'-': 0, '+': 0, '*': 1, '^': 2, 'cos': 3, 'sin': 3, 'ln': 3}
    for i in eq:
        if i not in symb:
            if i == 'x':
                s.append(x)
            else:
                s.append(i)
        else:
            if i == '-':
                a = s.pop()
                b = s.pop()
                s.append(b - a)
            elif i == '+':
                a = s.pop()
                b = s.pop()
                s.append(b + a)
            elif i == '*':
                a = s.pop()
                b = s.pop()
                s.append(b * a)
            elif i == '^':
                a = s.pop()
                b = s.pop()
                s.append(b ** a)
            elif i == 'cos':
                a = s.pop()
                s.append(np.cos(a))
            elif i == 'sin':
                a = s.pop()
                s.append(np.sin(a))
            elif i == 'ln':
                a = s.pop()
                if a <= 0:
                    raise ZeroDivisionError
                s.append(np.log(a))
    return s[0]


# Вычисление производной функции
def derivative(eq):
    d = []
    container = []
    i = 0
    while i < len(eq):
        if str(eq[i]) == '^':
            degree = eq[i - 1]
            if degree > 0:
                index = 0
                for j in range(len(container)):
                    if container[j] in ['^', '-', '+', '*']:
                        d.append(container[j])
                        index = j + 1
                    else:
                        break
                d.append(degree)
                d += container[index:-1]
                d.append(degree - 1)
                d.append('^')
                d.append('*')
                container = []
            else:
                d += container
                d.append("^")
                container = []
        elif str(eq[i]) == 'sin':
            d += container
            container = []
            d.append('cos')
        elif str(eq[i]) == 'cos':
            d.append(-1)
            d += container
            container = []
            d.append('sin')
            d.append('*')
            if i < len(eq) - 2 and str(eq[i + 1]) == '*':
                d.append('*')
                i += 1
        elif str(eq[i]) == 'x' and i < len(eq) - 3 and str(eq[i + 2]) != "^" and str(eq[i + 1]) != "sin" \
                and str(eq[i + 1]) != "cos":
            d += container
            container = []
            d.append('x')
            d.append(0)
            d.append('^')
        else:
            container.append(eq[i])
        i += 1
    for i in container:
        if str(i) in ['^', '-', '+', '*']:
            d.append(i)
        else:
            break
    return d


# Вычисление первообразной функции
def antiderivative(eq):
    d = []
    container = []
    i = 0
    while i < len(eq):
        if str(eq[i]) == '^':
            # print(container)
            degree = eq[i - 1]
            if degree != -1:
                index = 0
                for j in range(len(container)):
                    if container[j] == 'x':
                        index = j + 1
                        break
                d.append(1/(degree+1))
                # print(index)
                d += container[:index]
                d.append(degree + 1)
                d.append('^')
                d.append('*')
                container = []
            else:
                d += container[:-1]
                d.append("ln")
                container = []
        elif eq[i] in ['-', '+'] and eq[i-1] == '*' and 'x' in container:
            d.append(1/2)
            d.append(eq[i-3])
            d.append('x')
            d.append(2)
            d.append('^')
            d.append('*')
            d.append('*')
            d.append(eq[i])
            container = []
        elif eq[i] in ['-', '+'] and eq[i-1] in ['*', '^']:
            d.append(eq[i])
        elif eq[i] in ['-', '+'] and eq[i-1] != 'x':
            d.append(eq[i-1])
            d.append('x')
            d.append('*')
            d.append(eq[i])
            container = []
        elif eq[i] in ['-', '+']:
            if type(eq[i-2]) == float:
                d.append(eq[i - 2])
                d.append('x')
                d.append('*')
            d.append(1/2)
            d.append('x')
            d.append(2)
            d.append('^')
            d.append('*')
            d.append(eq[i])
            container = []
        elif eq[i] == '*' and 'x' not in container:
            d.append('*')
        elif str(eq[i]) == 'cos':
            d += container
            container = []
            d.append('sin')
        elif str(eq[i]) == 'sin':
            d.append(-1)
            d += container
            container = []
            d.append('cos')
            d.append('*')
            if i < len(eq) - 2 and str(eq[i + 1]) == '*':
                d.append('*')
                i += 1
        else:
            container.append(eq[i])
        i += 1
    for i in container:
        if str(i) in ['^', '-', '+', '*']:
            d.append(i)
        elif i == 'x':
            d.append(1 / 2)
            d.append('x')
            d.append(2)
            d.append('^')
            d.append('*')
        elif type(i) == float:
            d.append(i)
            d.append('x')
            d.append('*')
        else:
            break
    return d

