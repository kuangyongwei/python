class A(object):
    def __init__(self):
        self.n = 10

    def minus(self, m):
        self.n -= m


class B(A):
    def __init__(self):
        self.n = 7

    def minus(self, m):
        super(B, self).minus(m)
        self.n -= 2


b = B()
b.minus(2)
print(b.n)


class C(A):
    def __init__(self):
        self.n = 12

    def minus(self, m):
        super(C, self).minus(m)
        self.n -= 5


class D(B, C):
    def __init__(self):
        self.n = 15

    def minus(self, m):
        super(D, self).minus(m)  # n=15,m=2
        self.n -= 2


d = D()
d.minus(2)
print(d.n)
print(D.__mro__)
