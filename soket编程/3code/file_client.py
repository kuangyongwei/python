import socket


# 1. 产生tcp客户端的对象
def create_client(ip, port):
    client = socket.socket()
    client.connect_ex((ip, port))
    return client


def user_input_handler(user_data):
    return user_data.split(':')[0].strip()


def list_handler(dest_addr, user_data):
    res_data = b''
    client_sock = create_client(*dest_addr)
    ret = client_sock.send(user_data.encode('utf-8'))
    print("发送获取文件列表请求", ret)
    buf = client_sock.recv(1024)
    while buf:
        res_data += buf
        buf = client_sock.recv(1024)
    print("接收完成")
    import pickle
    res = pickle.loads(res_data)
    print(res)
    client_sock.close()


def getfile_handler(dest_addr, user_data):
    filename = user_data.split(':')[1].strip()
    client_sock = create_client(*dest_addr)
    ret = client_sock.send(user_data.encode('utf-8'))
    print("发送获取文件请求", ret)
    with open(filename, 'wb') as fp:
        buf = client_sock.recv(1024)
        while buf:
            fp.write(buf)
            buf = client_sock.recv(1024)
        client_sock.close()


def putfile_handler(dest_addr, user_data):
    total = 0
    filename = user_data.split(':')[1].strip()
    import os
    if not os.path.isfile(filename):
        print("文件不存在")
        return
    client_sock = create_client(*dest_addr)
    client_sock.send(user_data.encode('utf-8'))
    with open(filename, 'rb') as fp:
        buf = fp.read(1024)
        while buf:
            ret = client_sock.send(buf)
            total += ret
            buf = fp.read(1024)
        print("上传: ", total)
    client_sock.close()


def default_handler():
    print("请输入合法的参数请求")


def main_process():
    buf = input("请输入命令: ")
    dest_ip = '192.168.102.128'
    port = 9000
    while buf:
        flags = user_input_handler(buf)
        if flags == 'L':
            list_handler((dest_ip, port), buf)
        elif flags == 'G':
            getfile_handler((dest_ip, port), buf)
        elif flags == 'P':
            putfile_handler((dest_ip, port), buf)
        else:
            default_handler()
        buf = input("请输入命令: ")

    print("客户端关闭了")


if __name__ == '__main__':
    main_process()
