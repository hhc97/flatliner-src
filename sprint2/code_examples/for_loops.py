def test(loops):
    total = 0  # total is 0 at first
    # do the loop
    for i in range(loops):
        total = total + i
    return total


print(test(6))
