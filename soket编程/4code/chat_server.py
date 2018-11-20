import select
import socket
import sys


def create_listen_sock(port=8080):
    listen_fd = socket.socket()
    listen_fd.bind(('', port))
    listen_fd.listen(5)
    return listen_fd


def new_client_handler(new_fd: socket.socket):
    buf = new_fd.recv(1024)
    while buf:
        print("收到{} 消息: {}".format(new_fd.fileno(), buf.decode('utf-8')))
        buf = new_fd.recv(1024)
    new_fd.close()


def main_process(listen_fd: socket.socket):
    contact = {}
    uid = 1
    rlist = [listen_fd, sys.stdin]
    while True:
        res_read, _, _ = select.select(rlist, [], [])
        for x in res_read:
            if x is listen_fd:
                new_fd, _ = listen_fd.accept()
                print("新链接到来", new_fd)
                rlist.append(new_fd)
                contact[uid] = new_fd
                uid += 1
            elif x is sys.stdin:
                buf = input('')
                k = buf.split(':')[0].strip()
                sock = contact[int(k)]
                sock.send(buf.encode('utf-8'))
            else:
                buf = x.recv(1024)
                if buf:
                    print("收到:{},信息是 {}".format(x.fileno(), buf.decode('utf-8')))
                else:
                    x.close()
                    print("关闭连接")
                    rlist.remove(x)


if __name__ == '__main__':
    sock = create_listen_sock()
    main_process(sock)
