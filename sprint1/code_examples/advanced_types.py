"""
A test for advanced types.
"""


def test(a, b):
    for i in b:
        if i  == 1:
            a += 2
        else:
            a += i
    return a


a = test(0, [1, 1, 2])

print(a)
