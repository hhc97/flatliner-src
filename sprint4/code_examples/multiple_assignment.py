lst = [1, 2, 3, 4, 5]
print(lst)

# variable swapping
lst[0], lst[1] = lst[1], lst[0]
print(lst)
lst[2], lst[3], lst[4] = lst[4], lst[2], lst[3]
print(lst)

# mixed assignment
lst[1], b, c = 9, 10, 11
print(lst, b, c)

# multiple assignment
lst[0] = d = 6
print(lst, d)
lst[0] = lst[1] = lst[2] = 33
print(lst)


def test():
    t1, t2 = 9, 10
    t3, t4 = 11, 12
    return t1 + t4, t2 + t3


# assign to return value
e, f = test()
print(e, f)

g, h = lst[3] + lst[0], lst[4]
print(g, h)

temp = -5, -6, -7
i, j, k = temp
print(i, j, k)

lst2 = [5, 4, 3, 2, 1]
s1, s2, s3 = lst2[::-1][1:4]
print(s1, s2, s3)
for item in [[2, 5], [7, 8]]:
    lst2[0], lst2[3] = item
    l, m = item
    n, lst2[4] = item
    print(l, m, n)
    print(lst2)
print(lst2)

o, p = 10, 10
for num in [1, 2, 3]:
    print(o, p)
    o, p = num, num + 1
print(o, p)

hold = None
for thing in lst2:
    print(hold)
    hold = thing
print(hold)


class Tester:
    def __init__(self):
        self.x, self.y = 4, 5


test_inst = Tester()
for item in [[1, 2, 3], [6, 7, 8], [9, 10, 15]]:
    print(test_inst.x, test_inst.y)
    q, test_inst.x, test_inst.y = item
    print(q, test_inst.x, test_inst.y)

print(test_inst.x, test_inst.y)
print(q)

for r, s in [[[(1, 2), (9, 6)], 3], [[(6, 7), (4, 3)], 8]]:
    print(r, s)
    for t, u in r:
        print(t, u)
        if r[0][0] <= r[0][1] <= u < t:
            print('chained comparison!')
        if r[0][0] <= r[0][1] <= u < t > 20:
            print('chained comparison failed')

v, w = 11, 11
for x, y in [[3, 4], [4, 5]]:
    print(v, w)
    v, w = x, y
print(v, w)
