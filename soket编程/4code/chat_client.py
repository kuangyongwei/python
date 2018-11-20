import socket
import select
import sys


# 1. 产生tcp客户端的对象
def create_client(ip, port):
    client = socket.socket()
    client.connect_ex((ip, port))
    return client


# 2. 单链接聊天程序
def client_chat():
    client_fd = create_client('192.168.102.128', 8080)

    rlist = [sys.stdin, client_fd]
    while True:
        res, _, _ = select.select(rlist, [], [])
        for x in res:
            if x is sys.stdin:
                buf = input('')
                if buf.startswith('quit'):
                    client_fd.close()
                    return
                client_fd.send(buf.encode('utf-8'))
            elif x is client_fd:
                buf = client_fd.recv(1024)
                if buf:	
                    print("收到了服务器的消息: ", buf.decode('utf-8'))
                else:
                    x.close()
                    return


if __name__ == '__main__':
    client_chat()
