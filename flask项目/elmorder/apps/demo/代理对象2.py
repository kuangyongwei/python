"""
    ''' 定义一种类型的女人，王婆和潘金莲都属于这个类型的女人
        种女人能做什么事情呢？
        '''
    #抛媚眼
        # happy
"""


class KindWoman(object):

    def make_eyes_with_man(self):
        pass

    # 和男人那个...
    def happy_with_man(self):
        pass


# "定义一个潘金莲是什么样的人 "
class PanJinLian(KindWoman):
    def happy_with_man(self):
        print("潘金莲和男人在做那个...")

    def make_eyes_with_man(self):
        print("潘金莲抛媚眼...")


"""王婆这个人老聪明了，她太老了，
     是个男人都看不上她，
     但是她有智慧经验呀，
     他作为一类女人的代理！
"""


class WangPo(KindWoman):

    def __init__(self):
        self.kind_woman = PanJinLian()

    def set_kindWoman(self, kindWoman):
        '''她可以是KindWomam的任何一个女人的代理，
           只要你是这一类型
     '''
        self.kind_woman = kindWoman

    '''自己老了，干不了了，但可以叫年轻的代替'''

    def happy_with_man(self):
        self.kind_woman.happy_with_man()

    '''王婆年纪大了，谁看她抛媚眼啊'''

    def make_eyes_with_man(self):
        self.kind_woman.make_eyes_with_man()


class JiaShi(KindWoman):
    # "定义一个贾氏是什么样的人"
    def happy_with_man(self):
        print("贾氏和男人在做那个...")

    def make_eyes_with_man(self):
        print("贾氏抛媚眼...")


class XiMenQiang(object):
    # 水浒传是这样写的：西门庆被潘金莲用竹竿敲了一下，
    #     西门庆看痴迷了，被王婆看到了，就开始撮合两人好事，
    #     王婆作为潘金莲的代理人收了不少好处费，
    #     那我们假设一下：  *如果没有王婆在中间牵线，
    #     这两个不要脸的能成事吗？难说得很！

    def star(self):
        wangPo = WangPo()
        # 然后西门庆说，我要和潘金莲Happy,
        # 然后王婆就安排了西门庆丢筷子哪出戏：
        wangPo.make_eyes_with_man()
        # 看到没有表面是王婆在做，其实爽的是潘金莲
        wangPo.happy_with_man()

        # 王婆成了贾氏的代理了
        jiashi = JiaShi()
        wangPo.set_kindWoman(jiashi)
        wangPo.make_eyes_with_man()
        # 看到没有表面是王婆在做，其实爽的是潘金莲
        wangPo.happy_with_man()


XiMenQiang().star()
