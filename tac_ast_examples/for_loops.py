def test(loops):
    total = 0  # total is 0 at first
    # do the loop
    for i in range(loops):
        print('iteration', i, 'of loop')
        total = total + i
    return total


print('total sum =', test(6))
