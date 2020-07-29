import socket
import threading

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
DB_HOST = '127.0.0.1'
DB_PORT = 5432
PORT = 65431        # Port to listen on (non-privileged ports are > 1023)


def pipe(in_sock, out_sock):
    while True:
        _data = in_sock.recv(1024)
        if not _data:
            continue
        print(_data)
        out_sock.sendall(_data)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as receive_socket:
    receive_socket.bind((HOST, PORT))
    receive_socket.listen()
    receive_conn, addr = receive_socket.accept()

    with receive_conn:
        print('Connected by', addr, flush=True)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as send_socket:
            send_socket.connect((DB_HOST, DB_PORT))
            hin_thread = threading.Thread(target=pipe, args=(receive_conn, send_socket))
            ruck_thread = threading.Thread(target=pipe, args=(send_socket, receive_conn))

            hin_thread.start()
            ruck_thread.start()

            hin_thread.join()
            ruck_thread.join()
