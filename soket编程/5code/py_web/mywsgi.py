from datetime import datetime


# 定义WSGI规范的函数接口
def application(environ, start_respone):
    # 判断是什么请求
    if environ['name'] == '/time/':
        time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        status = 200
        respone_headers = [('Content-Type', 'text/plain')]
        start_respone(status, respone_headers)
        return time_str
    else:
        status = 200
        respone_headers = [('Content-Type', 'text/plain')]
        start_respone(status, respone_headers)
        return "<h1>Hello World</h1>"
