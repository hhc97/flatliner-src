def get_average_elevation(m: list[list[int]]) -> float:
    """
    Returns the average elevation across the elevation map m.

    Examples
    >>> get_average_elevation([])
    0
    >>> m = [[1,2,3],[4,5,6],[7,8,9]]
    >>> get_average_elevation(m)
    5.0
    >>> m = [[1,2,2,5],[4,5,4,8],[7,9,9,1],[1,2,1,4]]
    >>> get_average_elevation(m)
    4.0625
    """
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


def find_peak(m: list[list[int]]) -> list[int]:
    """
    Given an non-empty elevation map m, returns the cell of the
    highest point in m.

    Examples (note some spacing has been added for human readablity)
    >>> m = [[1,2,3],[9,8,7],[5,4,6]]
    >>> find_peak(m)
    [1, 0]
    >>> m = [[6,2,3],[1,8,7],[5,4,9]]
    >>> find_peak(m)
    [2, 2]
    """
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


def is_sink(m: list[list[int]], c: list[int]) -> bool:
    """
    Returns True if and only if c is a sink in m.

    Examples (note some spacing has been added for human readablity)
    >>> m = [[1,2,3],[2,3,3],[5,4,3]]
    >>> is_sink(m, [0,0])
    True
    >>> is_sink(m, [2,2])
    True
    >>> is_sink(m, [3,0])
    False
    >>> m = [[1,2,3],[2,1,3],[5,4,3]]
    >>> is_sink(m, [1,1])
    True
    """
    # Your code goes here
    if c[0] == 0 and c[1] == 0:
        if (m[c[0]][c[1]] <= m[c[0] + 1][c[1]] and m[c[0]][c[1]] <= m[c[0]][c[1] + 1] and
                m[c[0]][c[1]] <= m[c[0] + 1][c[1] + 1]):
            return True
    if c[0] == 0 and c[1] > 0 and c[1] < (len(m[0]) - 1):
        if (m[c[0]][c[1]] <= m[c[0]][c[1] - 1] and m[c[0]][c[1]] <= m[c[0]][c[1] + 1] and
                m[c[0]][c[1]] <= m[c[0] + 1][c[1] - 1] and m[c[0]][c[1]] <= m[c[0] + 1][c[1]] and
                m[c[0]][c[1]] <= m[c[0] + 1][c[1] + 1]):
            return True
    if c[0] == 0 and c[1] == (len(m[0]) - 1):
        if (m[c[0]][c[1]] <= m[c[0]][c[1] - 1] and m[c[0]][c[1]] <= m[c[0] + 1][c[1] - 1] and
                m[c[0]][c[1]] <= m[c[0] + 1][c[1]]):
            return True
    if c[0] > 0 and c[0] < (len(m) - 1) and c[1] == 0:
        if (m[c[0]][c[1]] <= m[c[0] - 1][c[1]] and m[c[0]][c[1]] <= m[c[0] - 1][c[1] + 1] and
                m[c[0]][c[1]] <= m[c[0]][c[1] + 1] and m[c[0]][c[1]] <= m[c[0] + 1][c[1] + 1] and
                m[c[0]][c[1]] <= m[c[0] + 1][c[1]]):
            return True
    if c[0] > 0 and c[0] < (len(m) - 1) and c[1] > 0 and c[1] < (len(m[0]) - 1):
        if (m[c[0]][c[1]] <= m[c[0] - 1][c[1] - 1] and m[c[0]][c[1]] <= m[c[0] - 1][c[1]] and
                m[c[0]][c[1]] <= m[c[0] - 1][c[1] + 1] and m[c[0]][c[1]] <= m[c[0]][c[1] - 1] and
                m[c[0]][c[1]] <= m[c[0]][c[1] + 1] and m[c[0]][c[1]] <= m[c[0] + 1][c[1] - 1] and
                m[c[0]][c[1]] <= m[c[0] + 1][c[1]] and m[c[0]][c[1]] <= m[c[0] + 1][c[1] + 1]):
            return True
    if c[0] > 0 and c[0] < (len(m) - 1) and c[1] == (len(m[0]) - 1):
        if (m[c[0]][c[1]] <= m[c[0] - 1][c[1]] and m[c[0]][c[1]] <= m[c[0] - 1][c[1] - 1] and
                m[c[0]][c[1]] <= m[c[0]][c[1] - 1] and m[c[0]][c[1]] <= m[c[0] + 1][c[1] - 1] and
                m[c[0]][c[1]] <= m[c[0] + 1][c[1]]):
            return True
    if c[0] == (len(m) - 1) and c[1] == 0:
        if (m[c[0]][c[1]] <= m[c[0] - 1][c[1]] and m[c[0]][c[1]] <= m[c[0] - 1][c[1] + 1] and
                m[c[0]][c[1]] <= m[c[0]][c[1] + 1]):
            return True
    if c[0] == (len(m) - 1) and c[1] > 0 and c[1] < (len(m[0]) - 1):
        if (m[c[0]][c[1]] <= m[c[0]][c[1] - 1] and m[c[0]][c[1]] <= m[c[0] - 1][c[1] - 1] and
                m[c[0]][c[1]] <= m[c[0] - 1][c[1]] and m[c[0]][c[1]] <= m[c[0] - 1][c[1] + 1] and
                m[c[0]][c[1]] <= m[c[0]][c[1] + 1]):
            return True
    if c[0] == (len(m) - 1) and c[1] == (len(m[0]) - 1):
        if (m[c[0]][c[1]] <= m[c[0]][c[1] - 1] and m[c[0]][c[1]] <= m[c[0] - 1][c[1] - 1] and
                m[c[0]][c[1]] <= m[c[0] - 1][c[1]]):
            return True
    return False


def can_hike_to(m: list[list[int]], s: list[int], d: list[int], supplies: int) -> bool:
    """
    Given an elevation map m, a start cell s, a destination cell d, and
    the an amount of supplies returns True if and only if a hiker could reach
    d from s using the strategy dscribed in the assignment .pdf. Read the .pdf
    carefully. Assume d is always south, east, or south-east of s. The hiker
    never travels, north, west, nor backtracks.

    Examples (note some spacing has been added for human readablity)
    >>> m = [[1,4,3],
             [2,3,5],
             [5,4,3]]
    >>> can_hike_to(m, [0,0], [2,2], 4)
    True
    >>> can_hike_to(m, [0,0], [0,0], 0)
    True
    >>> can_hike_to(m, [0,0], [2,2], 3)
    False
    >>> m = [[1,  1,100],
             [1,100,100],
             [1,  1,  1]]
    >>> can_hike_to(m, [0,0], [2,2], 4)
    False
    >>> can_hike_to(m, [0,0], [2,2], 202)
    True
    """
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
