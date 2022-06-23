def get_average_elevation(m):
    # Your code goes here
    total = 0
    n = 0
    for lst in m:
        for i in lst:
            total = total + i
            n = n + 1
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

sample = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
print(get_average_elevation(sample))
print(find_peak(sample))

