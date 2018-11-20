# -*- coding:utf-8 -*-

class CallInfo(object):
    '''封装一次函数调用信息。'''

    def __init__(self, obj_name, func_name, *args, **kawrgs):
        '''调用是这样的：
        obj_name.func_name(*args, **kwargs)
        '''
        self.obj = obj_name
        self.func = func_name
        self.args = args
        self.kwargs = kawrgs

    def __str__(self):
        return "obj=%s, func=%s, args=%s, kwargs=%s" % (self.obj, self.func, self.args, self.kwargs)


class FuncProxy(object):
    def __init__(self, target_name, call_info_processor):
        self.__target_name = target_name
        self.__call_info_processor = call_info_processor

    def __getattribute__(self, name):
        if name.startswith("_"):
            return super(FuncProxy, self).__getattribute__(name)

        def trigger_func(*args, **kwargs):
            call_info = CallInfo(self.__target_name, name, *args, **kwargs)
            self.__call_info_processor(call_info)

        return trigger_func


class RemoteObjectProxy(object):
    '''该类可接受任意函数调用，再将该调用封装为CallInfo，发送到远端。
    远端可能是另一台机器或另一个进程等。
    '''

    # 省略其他通信部分
    # .....
    # ----------------------------
    def __call__(self, call_target, proxy=False):
        '''生成FuncProxy类型代理对象。proxy应为True。'''
        if proxy:
            return FuncProxy(call_target, self.send_func_call)

    def send_func_call(self, call_info):
        # 省略发送call_info到远端的具体通信，用print代替
        print("Sending call_info is %s" % str(call_info))



if __name__ == "__main__":
    proxy = RemoteObjectProxy()
    proxy("a_remote_object", proxy=True).foo("paramA", "paramB", key_param=123, key_param2=456)
