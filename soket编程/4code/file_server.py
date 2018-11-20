import socket
import os


ROOT_PATH = '/home/dev1/share/'
UPLOAD_PATH = '/home/dev1/uploads/'


def create_listen_sock(port=8080):
    listen_fd = socket.socket()
    listen_fd.bind(('', port))
    listen_fd.listen(5)
    return listen_fd


def parse_client_data(data: bytes):
    return data.split(b':')[0].strip()


def download_handler(client_sock, data: bytes):
    total = 0
    filename = data.split(b':')[1].strip().decode('utf-8')
    file_path = os.path.join(ROOT_PATH, filename)
    print("服务器下载文件信息:", file_path)
    if not os.path.isfile(file_path):
        client_sock.close()

    with open(file_path, 'rb') as fp:
        buf = fp.read(1024)
        while buf:
            ret = client_sock.send(buf)
            total += ret
            buf = fp.read(1024)
        print("总共发送", total)


def list_handler(client_sock):
    import pickle
    res = os.listdir(ROOT_PATH)
    data = pickle.dumps(res)
    ret = client_sock.send(data)
    print("发送了", ret)


def put_handler(t_sock, data: bytes):
    filename = data.split(b':')[1].strip().decode('utf-8')
    file_path = os.path.join(UPLOAD_PATH, filename)

    with open(file_path, 'wb') as fp:
        buf = t_sock.recv(1024)
        while buf:
            fp.write(buf)
            buf = t_sock.recv(1024)
    print("上传成功")

def main_process(listen_fd: socket.socket):
    new_fd, _ = listen_fd.accept()
    print("新链接到来", new_fd)
    buf = new_fd.recv(1024)
    flags = parse_client_data(buf)
    if flags == b'G':
        download_handler(new_fd, buf)
    elif flags == b'L':
        list_handler(new_fd)
    elif flags == b'P':
        put_handler(new_fd, buf)
    new_fd.close()


if __name__ == '__main__':
    sock = create_listen_sock(9000)
    while True:
        main_process(sock)
