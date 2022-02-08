"""
A function definition with a function call.
Test comments with weird characters:
!"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~
"""


def test(loops: int) -> int:
    total = 0  # total is 0 at first
    # do the loop
    for i in range(loops):
        total += i
    return total


print(test(6))
