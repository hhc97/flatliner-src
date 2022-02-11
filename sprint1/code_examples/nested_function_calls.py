def test1(a, b):
    """A function"""
    return a + b


def test2(c, d):
    """Another function"""
    return c + d


e = test1(test2(1, 2), test2(3, 4))
print(e)
