def test(a, b):
    new = []
    for i in b:
        if i == 2:
            new.append(i)
        else:
            new.append(i + a)
    return new


c = test(5, [1, 2, 3, 4, 5])

print(c)
