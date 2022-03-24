def get_average_elevation(m):
    # Your code goes here
    total = 0
    n = 0
    for lst in m:
        for i in lst:
            total = total + i
            n += 1
    if n == 0:
        return 0
    return total / n


def find_peak(m):
    # Your code goes here
    largest = 0
    x = 0
    y = 0
    for data in m:
        for i in range(len(data)):
            if data[i] > largest:
                x = m.index(data)
                y = i
                largest = data[i]
    return [x, y]


def is_sink(m, c):
    # Your code goes here
    if c[0] == 0 and c[1] == 0:
        if (m[c[0]][c[1]] <= m[c[0] + 1][c[1]] and m[c[0]][c[1]] <= m[c[0]][c[1] + 1] and m[c[0]][c[1]] <= m[c[0] + 1][c[1] + 1]):
            return True
    if c[0] == 0 and c[1] > 0 and c[1] < (len(m[0]) - 1):
        if (m[c[0]][c[1]] <= m[c[0]][c[1] - 1] and m[c[0]][c[1]] <= m[c[0]][c[1] + 1] and m[c[0]][c[1]] <= m[c[0] + 1][c[1] - 1] and m[c[0]][c[1]] <= m[c[0] + 1][c[1]] and m[c[0]][c[1]] <= m[c[0] + 1][c[1] + 1]):
            return True
    if c[0] == 0 and c[1] == (len(m[0]) - 1):
        if (m[c[0]][c[1]] <= m[c[0]][c[1] - 1] and m[c[0]][c[1]] <= m[c[0] + 1][c[1] - 1] and m[c[0]][c[1]] <= m[c[0] + 1][c[1]]):
            return True
    if c[0] > 0 and c[0] < (len(m) - 1) and c[1] == 0:
        if (m[c[0]][c[1]] <= m[c[0] - 1][c[1]] and m[c[0]][c[1]] <= m[c[0] - 1][c[1] + 1] and m[c[0]][c[1]] <= m[c[0]][c[1] + 1] and m[c[0]][c[1]] <= m[c[0] + 1][c[1] + 1] and m[c[0]][c[1]] <= m[c[0] + 1][c[1]]):
            return True
    if c[0] > 0 and c[0] < (len(m) - 1) and c[1] > 0 and c[1] < (len(m[0]) - 1):
        if (m[c[0]][c[1]] <= m[c[0] - 1][c[1] - 1] and m[c[0]][c[1]] <= m[c[0] - 1][c[1]] and m[c[0]][c[1]] <= m[c[0] - 1][c[1] + 1] and m[c[0]][c[1]] <= m[c[0]][c[1] - 1] and m[c[0]][c[1]] <= m[c[0]][c[1] + 1] and m[c[0]][c[1]] <= m[c[0] + 1][c[1] - 1] and m[c[0]][c[1]] <= m[c[0] + 1][c[1]] and m[c[0]][c[1]] <= m[c[0] + 1][c[1] + 1]):
            return True
    if c[0] > 0 and c[0] < (len(m) - 1) and c[1] == (len(m[0]) - 1):
        if (m[c[0]][c[1]] <= m[c[0] - 1][c[1]] and m[c[0]][c[1]] <= m[c[0] - 1][c[1] - 1] and m[c[0]][c[1]] <= m[c[0]][c[1] - 1] and m[c[0]][c[1]] <= m[c[0] + 1][c[1] - 1] and m[c[0]][c[1]] <= m[c[0] + 1][c[1]]):
            return True
    if c[0] == (len(m) - 1) and c[1] == 0:
        if (m[c[0]][c[1]] <= m[c[0] - 1][c[1]] and m[c[0]][c[1]] <= m[c[0] - 1][c[1] + 1] and m[c[0]][c[1]] <= m[c[0]][c[1] + 1]):
            return True
    if c[0] == (len(m) - 1) and c[1] > 0 and c[1] < (len(m[0]) - 1):
        if (m[c[0]][c[1]] <= m[c[0]][c[1] - 1] and m[c[0]][c[1]] <= m[c[0] - 1][c[1] - 1] and m[c[0]][c[1]] <= m[c[0] - 1][c[1]] and m[c[0]][c[1]] <= m[c[0] - 1][c[1] + 1] and m[c[0]][c[1]] <= m[c[0]][c[1] + 1]):
            return True
    if c[0] == (len(m) - 1) and c[1] == (len(m[0]) - 1):
        if (m[c[0]][c[1]] <= m[c[0]][c[1] - 1] and m[c[0]][c[1]] <= m[c[0] - 1][c[1] - 1] and m[c[0]][c[1]] <= m[c[0] - 1][c[1]]):
            return True
    return False


def can_hike_to(m, s, d, supplies):
    # Your code goes here
    while s != d and s[0] < (len(m) - 1) and s[1] < (len(m[0]) - 1) and supplies >= 0 and s[0] < d[0] and s[1] < d[1]:
        if abs(m[s[0]][s[1]] - m[s[0]][s[1] + 1]) <= abs(m[s[0]][s[1]] - m[s[0] + 1][s[1]]):
            supplies = supplies - abs(m[s[0]][s[1]] - m[s[0]][s[1] + 1])
            s[1] = s[1] + 1
        else:
            supplies = supplies - abs(m[s[0]][s[1]] - m[s[0] + 1][s[1]])
            s[0] = s[0] + 1
    while s != d and s[0] == (len(m) - 1) and supplies >= 0:
        supplies = supplies - abs(m[s[0]][s[1]] - m[s[0]][s[1] + 1])
        s[1] = s[1] + 1
    while s != d and s[1] == (len(m[0]) - 1) and supplies >= 0:
        supplies = supplies - abs(m[s[0]][s[1]] - m[s[0] + 1][s[1]])
        s[0] = s[0] + 1
    while s != d and s[0] < d[0] and s[1] == d[1] and supplies > 0:
        supplies = supplies - abs(m[s[0]][s[1]] - m[s[0] + 1][s[1]])
        s[0] = s[0] + 1
    while s != d and s[0] == d[0] and s[1] < d[1] and supplies > 0:
        supplies = supplies - abs(m[s[0]][s[1]] - m[s[0]][s[1] + 1])
        s[1] = s[1] + 1
    if supplies < 0:
        return False
    if s == d and supplies >= 0:
        return True


sample = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(get_average_elevation(sample))
print(find_peak(sample))
print(is_sink(sample, [1, 1]))
print(is_sink(sample, [0, 0]))
print(can_hike_to(sample, [0, 0], [2, 2], 8))
print(can_hike_to(sample, [0, 0], [2, 2], 4))
