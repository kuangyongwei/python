"""
回调函数
"""


def fun():
    print("开始发送响应数据")
    return "success"


def web_loop(fn):
    print("web服务器开始运行")
    import time
    time.sleep(1)
    print("连接来到,处理请求")
    ret = fn()
    send(ret)
    fn()
    fn()
    fn()
    fn()
    fn()


web_loop(fun)

fun()

