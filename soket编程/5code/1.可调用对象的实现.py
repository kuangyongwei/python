class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __call__(self, *args, **kwargs):
        print("=======")


p = Person('jim', 18)
print(p.name)

print(p())

