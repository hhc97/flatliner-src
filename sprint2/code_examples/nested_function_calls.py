def test1(a, b):
    return a + b


def test2(c, d):
    return c + d


e = test1(test2(1, 2), test2(3, 4))
print(e)
