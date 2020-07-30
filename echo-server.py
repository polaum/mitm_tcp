import socket
import threading

HOST = '127.0.0.1'
DB_HOST = ''
DB_PORT = 8635
PORT = 65431        # Port to listen on (non-privileged ports are > 1023)


def pipe(in_sock, out_sock):
    while True:
        try:
            _data = in_sock.recv(1024)
            if not _data:
                continue
            print(_data, flush=True)
            out_sock.sendall(_data)
        except ConnectionResetError:
            continue


receive_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
receive_socket.bind((HOST, PORT))
receive_socket.listen()
print(f'Listening on {HOST}:{PORT}', flush=True)

while True:
    receive_conn, addr = receive_socket.accept()
    print('Connected by', addr, flush=True)
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    send_socket.connect((DB_HOST, DB_PORT))
    hin_thread = threading.Thread(target=pipe, args=(receive_conn, send_socket))
    ruck_thread = threading.Thread(target=pipe, args=(send_socket, receive_conn))
    hin_thread.start()
    ruck_thread.start()
