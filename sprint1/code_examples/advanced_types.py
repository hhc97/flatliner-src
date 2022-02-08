"""
A test for advanced types.
"""


def test(a: dict[int, int], b: list[int]) -> None:
    for i in b:
        if i in a:
            a[i] += 1
        else:
            a[i] = 1


temp = {}
test(temp, [1, 1, 2])

print(temp)
