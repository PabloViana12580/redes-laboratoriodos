import socket

HOST = "127.0.0.1"
PORT = 9090

def listen():
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind((HOST, PORT))
    connection.listen(10)
    print("Receptor listo para recepción de mensajes")
    while True:
        current_connection, address = connection.accept()
        while True:
            data = current_connection.recv(2048)

            if data == 'salir\r\n':
                current_connection.shutdown(1)
                current_connection.close()
                exit()

            elif data:
                current_connection.send(data)
                print(data)


if __name__ == "__main__":
    try:
        listen()
    except KeyboardInterrupt:
        pass