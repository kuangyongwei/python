class Dept(object):

    def __init__(self, name):
        self.name = name

    # target是拥有此属性的对象
    def __get__(self, target, type=None):
        # 默认返回self与obj都可以
        return 'Dept'


class Company(object):
    #   一定要作为类属性，作为实例属性无效
    dept = Dept('organ')


# 现在的测试结果
x = Company()
y = Dept("hello")
print(y.name)
#   返回True
print(x.dept)
print(type(x.dept) == str)
