def count_finite_differences(x_table, y_table, size):
    table = [['№', '   x_i   ', '  y_i   ']]
    for i in range(3, size+2):
        table[0].append(' ∆^'+str(i-2)+'y_i ')
    for i in range(size):
        table.append([i+1, x_table[i], y_table[i]])
    a = size - 1
    while a > 0:
        for i in range(a):
            table[i+1].append(table[i + 2][-1] - table[i+1][-1])
        a -= 1
    return table
