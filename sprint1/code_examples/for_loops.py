def test(loops: int) -> int:
    total = 0
    for i in range(loops):
        total += i
    return total


print(test(6))
