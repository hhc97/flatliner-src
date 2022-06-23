class Parent1:
    def method1(self):
        print(1)


class Parent2:
    def method2(self):
        print(2)


def factory():
    class Parent4:
        def method4(self):
            print(4)

    return Parent4


class Child(Parent1, Parent2, factory()):
    def method3(self):
        print(3)


child = Child()
child.method1()
child.method2()
child.method3()
child.method4()


class Child2(Child):
    def method5(self):
        print(5)


child2 = Child2()
child2.method1()
child2.method2()
child2.method3()
child2.method4()
child2.method5()
