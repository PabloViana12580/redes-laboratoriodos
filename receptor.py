"""
Universidad del Valle de Guatemala
Redes
Catedrático: Vinicio Paz
Pablo Viana - 16091
Sergio Marchena - 16
"""

import socket
import pickle
import binascii

HOST = "127.0.0.1"
PORT = 9090
HEADER_LENGTH = 10

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
connection.bind((HOST, PORT))
connection.listen(10)
sinruido = []
print("Receptor listo para recepción de mensajes")

def capa_verificacion(message):
    prefix = "0b"
    try:
        msg = message.to01()
        #total_msg = "".join((prefix, msg))
        n = int(msg, 2)
        ascii_string = binascii.unhexlify('%x' % n)
        return ascii_string
    except:
        return False
    """
    byte_number = toint.bit_length() + 7 // 8
    binary_array = toint.to_bytes(byte_number, "big")
    ascii_text = binary_array.decode()
    print(ascii_text)
    """

def capa_decodificacion(current_connection, header):

        message_length  = int(header.decode('utf-8').strip())
        data = pickle.loads(current_connection.recv(message_length))
        return {"header": header, "data": data}

def listen():
    while True:
        current_connection, address = connection.accept()
        while True:
            #------------ CAPA DE TRANSMISION ------------
            try:
                data = current_connection.recv(HEADER_LENGTH)
            except:
                continue
            # --------------------------------------------

            msgtrans = capa_decodificacion(current_connection, data)
            msgdecode = capa_verificacion(msgtrans['data']['message'])

            #------------ CAPA DE APLICACION ------------
            if msgdecode is False:
                continue
            else:
                print(msgdecode.decode('utf-8'))

            if msgtrans['data']['type'] == 'mensaje_sin_ruido':
                sinruido.append(msgdecode.decode('utf-8'))

            print(msgtrans['data']['bits'])
            print(type(msgtrans['data']['bits']))

            if msgtrans['data']['bits'] > 100 == 0:
                print("mensaje sin ruido")
                print(sinruido.pop())
                print("mensaje con ruido")
                print(msgdecode.decode('utf-8'))


            if data == 'salir\r\n':
                current_connection.shutdown(1)
                current_connection.close()
                exit()


if __name__ == "__main__":
    try:
        listen()
    except KeyboardInterrupt:
        pass