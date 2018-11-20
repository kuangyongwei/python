import socket


# 1. 创建监听描述符对象,目的把服务器的IP和端口对外开放出来
# 等待客户端的链接
def create_listen_sock(port=8080):
    listen_fd = socket.socket()
    listen_fd.bind(('', port))
    listen_fd.listen(5)
    return listen_fd


# 2. 等待客户端的三次握手的链接,获取新描述符对象
# 依靠这个新描述符对象进行IO处理
def main_process(listen_fd: socket.socket):
    new_fd, _ = listen_fd.accept()
    print("新链接到来", new_fd)
    while True:
        buf = new_fd.recv(1024)
        if buf.decode('utf-8').startswith('quit'):
            break
        print(buf.decode('utf-8'))


if __name__ == '__main__':
    sock = create_listen_sock()
    # run_loop
    while True:
        main_process(sock)
