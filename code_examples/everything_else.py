import os as renamed_import
from sys import version as ver

import math

print(renamed_import.sep)
print(ver)

a = {0: 0}
a[5] = 0
a[6] = 2
b = 9
a[b] = 60
print(a)

c = {1, 2}
c |= {3, 4}
print(c)
c &= {1, 4}
print(c)


def test(d):
    def another(one, two):
        return one + two

    d[78] = [1, 2, list([5]), not True]
    if d:
        return another(d[78][-1], 2)
    return 6


x = 5
y = 2
while x < 20:
    if x > 5:
        x = x + y
        y = 2 * y
        print('in if')
    else:
        x = y + x
        y = x
        print('in else')
print(x)

x = 0
while x < 5:
    if x % 2 == 0:
        print('even')
    else:
        print('odd')
    print('looped', x)
    x = x + 1
print('done')

running = True
while running:
    brand_new_var = 2 + 6
    if brand_new_var > 5:
        running = False
    print(brand_new_var)
print('loop done')


def test_return_in_while():
    while True:
        return 6


print(test_return_in_while())


def test_while_stop():
    running = True
    x = 5
    d = {}
    while running:
        if x > 50:
            return d
        d[x] = [1, 2, 3]
        x = x + 10


print(test_while_stop())

x = 0
y = 5
while x < 10:
    y = x
    x = x + 5
    print(x, y)

e = test(a)
print(a, e)

while a[0] < 10:
    a[0] = a[0] + 3
    print(a[0] + a[5])
print(a[0])

a = [[1, 2, 3], 2, 3]
for item in a[0]:
    b = 5
    print(item + b)
print('done for loop')


def one():
    return 6


def two():
    return 8


x = 5
while one() and x < 20 or False:
    test = None
    if x > 10:
        test = one
    else:
        test = two
    x = x + 8
    print(test())
print('here1')

c = ('t', 'u', 'p', 'l', 'e')
d = c[0] + ''.join(c[1:-1]) + c[-1]
print(d)
print(math.e)

assert one() and two(), 'three'


class TestClass:
    def __init__(self):
        self.var = 'value'
        self.x = 0

    def test_method(self, thing):
        return self.var + thing

    def test_recursive_method(self, n):
        if n > 5:
            assert n > 5, 'oops'
            return self.test_recursive_method(n / 2)
        return self.test_method(str(n))

    def test_recursive_create(self):
        return TestClass()

    def test_default_param_method(self, p1, p2=5):
        return p1 + p2


testclass = TestClass()
testclass2 = testclass.test_recursive_create()
print(testclass.test_method(' added!'))
print(testclass.test_recursive_method(15))

print(testclass.x, testclass2.x)
for thing in [testclass, testclass2]:
    thing.x = 2
print(testclass.x, testclass2.x)
testclass.x = 10
print(testclass.x, testclass2.x)

print(testclass.test_default_param_method(1, 2))
print(testclass.test_default_param_method(1))


def test_default_param_func(p1, p2='hello', p3='world'):
    return ' '.join([p1, p2, p3])


print(test_default_param_func('test1'))
print(test_default_param_func('test2', p3='python!'))

a = 0
while a < 5:
    b = 0
    while b < 5:
        b = b + 1
        print(b)
    a = a + 1
    b = 0
    print(a)
print('done')


def rotate_matrix(matrix):
    new_matrix = []
    for i in range(len(matrix)):
        new_matrix.append([0] * len(matrix[0]))
    for x in range(len(matrix)):
        for y in range(len(matrix[0])):
            new_matrix[y][len(matrix) - x - 1] = matrix[x][y]
    return new_matrix


to_rotate = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
rotated = rotate_matrix(to_rotate)
print(rotated)

rotated += [1]
print(rotated)
rotated[0][0] += 2
print(rotated)

for i in range(5):
    while i < 6:
        i += 2
        print(i)
        for j in range(2):
            print('j')
    print('main')
print('done')

a = [1, 2, 3]
for i in range(len(a)):
    a[i] += 2
print(a)


def sum_list_recursive(lst):
    if len(lst) == 1:
        return lst[0]
    else:
        pass
    lst[0] += lst[-1]
    return sum_list_recursive(lst[:-1])


print(sum_list_recursive(list(range(15))))


def do_twice(func):
    def wrapper_do_twice():
        func()
        func()

    return wrapper_do_twice


def extra_print(num_times):
    def repeat_print(func):
        def wrapper_repeat():
            func()
            for i1 in range(num_times):
                print('extra print', i1)

        return wrapper_repeat

    return repeat_print


@extra_print(num_times=3)
@do_twice
@extra_print(num_times=2)
def double_print():
    print('double printer')


double_print()

print(one() if False else two())


class BinarySearchTree:
    # test recursive init method of class
    def __init__(self, root) -> None:
        """Initialize a new BST containing only the given root value.

        If <root> is None, initialize an empty tree.
        """
        if root is None:
            self._root = None
            self._left = None
            self._right = None
        else:
            self._root = root
            self._left = BinarySearchTree(None)
            self._right = BinarySearchTree(None)

    def is_empty(self) -> bool:
        return self._root is None


print(BinarySearchTree(10)._right is None)
print(BinarySearchTree(10)._right.is_empty())

a = not (not True or not False)
print(a)

single_tuple = (1,)
print(type(single_tuple))

[a, b] = [1, 2]
print(a, b)
[a,b] = {3:5, 4:6}
print(a, b)
