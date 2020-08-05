"""
Universidad del Valle de Guatemala
Redes
Catedrático: Vinicio Paz
Pablo Viana - 16091
Sergio Marchena - 16387
"""

import socket
import pickle
import binascii
from bitarray import bitarray
import hamming_code as hc

HOST = "127.0.0.1"
PORT = 9090
HEADER_LENGTH = 10

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
connection.bind((HOST, PORT))
connection.listen(10)
print("Receptor listo para recepción de mensajes")

def capa_verificacion(message):
    """ esta funcion decodifica los bits en caracteres ascii """
    prefix = "0b"
    msg = message.to01()
    #total_msg = "".join((prefix, msg))
    n = int(msg, 2)
    ascii_string = binascii.unhexlify('%x' % n)
    return ascii_string

def capa_decodificacion(current_connection, header):
    """ esta funcion se encarga de decodificar el mensaje para retornar un diccionario"""
    message_length  = int(header.decode('utf-8').strip())
    data = pickle.loads(current_connection.recv(message_length))
    return {"header": header, "data": data}

def listen():
    bandera = True
    hammin_flag = True
    while bandera:
        current_connection, address = connection.accept()
        while True:
            try:
                #------------ CAPA DE TRANSMISION ------------
                data = current_connection.recv(HEADER_LENGTH)
                # --------------------------------------------

                msgtrans = capa_decodificacion(current_connection, data)
                msgdecode = capa_verificacion(msgtrans['data']['message'])

                #------------ CAPA DE APLICACION ------------
                print("\n-------------> cantidad de bits transferidos: ", msgtrans['data']['bits'])
                print("mensaje tipo: ", msgtrans['data']['type'])
                print("se recibe: ", msgdecode)
                print("-----------------------------------------------")

                if(hammin_flag):
                    if msgtrans['data']['type'] == 'mensaje_sin_ruido':
                        r = hc.calcRedundantBits(len(msgtrans['data']['message'].to01()))
                        msg = msgtrans['data']['message'].to01()
                        # Determine the positions of Redundant Bits 
                        arr = hc.posRedundantBits(msg, r) 
                        # Determine the parity bits 
                        arr = hc.calcParityBits(arr, r)

                    if msgtrans['data']['type'] == 'mensaje_con_ruido':
                        correction = hc.detectError(msgtrans['data']['message'].to01(), r)
                        print("array de bits con hamming sin error: ", arr)
                        msg2 = msgtrans['data']['message'].to01()
                        # Determine the positions of Redundant Bits 
                        arr2 = hc.posRedundantBits(msg2, r) 
                        # Determine the parity bits 
                        arr2 = hc.calcParityBits(arr2, r)
                        print("array de bits con hamming con error: ", arr2)
                        print("La posicion del error es " + str(correction))

#\r\n
                if msgdecode.decode() == 'salir':
                    print("hasta pronto")
                    current_connection.shutdown(1)
                    current_connection.close()
                    bandera = False
                    break
                    exit()
                # --------------------------------------------
            except:
                continue

if __name__ == "__main__":
    try:
        listen()
    except KeyboardInterrupt:
        print("hasta pronto")
        exit()