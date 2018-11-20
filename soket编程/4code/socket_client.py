import socket


# 1. 产生tcp客户端的对象
def create_client(ip, port):
    client = socket.socket()
    client.connect_ex((ip, port))
    return client


# 2. 单链接聊天程序
def client_chat():
    client_fd = create_client('192.168.102.128', 8080)
    # client_fd = create_client('www.baidu.com', 80)
    buf = input('请输入聊天内容: ')
    while not buf.startswith('quit'):
        client_fd.send(buf.encode('utf-8'))
        buf = input('请输入聊天内容: ')
    client_fd.close()


# 3. 百度服务链接
def baidu_client():
    client_fd = create_client('www.baidu.com', 80)
    print("链接百度成功")
    request_data = "GET / HTTP/1.0\r\nHost: www.baidu.com\r\nConnection: closed\r\n\r\n"
    ret = client_fd.send(request_data.encode('utf-8'))
    print("发送成功了", ret)
    print("等待响应内容:")
    buf = client_fd.recv(1024)
    print("收到的:", buf)


if __name__ == '__main__':
    client_chat()

