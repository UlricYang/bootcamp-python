class A(object):
    def foo(self, x):
        print("executing foo(%s,%s)" % (self, x))
        print("self:", self)

    @classmethod
    def class_foo(cls, x):
        print("executing class_foo(%s,%s)" % (cls, x))
        print("cls:", cls)

    @staticmethod
    def static_foo(x):
        print("executing static_foo(%s)" % x)


a = A()

print(a.foo)
print(a.class_foo)
print(a.static_foo)

print()
a.foo(1)
a.class_foo(2)
a.static_foo(3)

print()
A.foo(a, 4)
A.class_foo(5)
A.static_foo(6)
