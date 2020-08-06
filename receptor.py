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
import time

HOST = "127.0.0.1"
PORT = 9090
HEADER_LENGTH = 10
array_hamming = []
paritybits_time = []
detection_times = []
r = 0

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
connection.bind((HOST, PORT))
connection.listen(10)
print("Receptor listo para recepción de mensajes")

def capa_verificacion(msgtrans):
    """ esta funcion decodifica los bits en caracteres ascii """
    global r
    global array_hamming
    global paritybits_time
    global detection_times
    hamming_flag = True
    message_str = msgtrans['data']['message'].to01()
    n = int(message_str, 2)
    ascii_string = binascii.unhexlify('%x' % n)

    if(hamming_flag):
        if msgtrans['data']['type'] == 'mensaje_sin_ruido':
            start = time.time()
            r = hc.calcRedundantBits(len(message_str))
            # Determine the positions of Redundant Bits
            arr = hc.posRedundantBits(message_str, r)
            # Determine the parity bits
            arr = hc.calcParityBits(arr, r)
            end = time.time()
            paritybits_time.append(end - start)
            array_hamming.append(arr)

        elif msgtrans['data']['type'] == 'mensaje_con_ruido':
            print("\nAlgoritmo de correccion de hamming")
            start_detection = time.time()
            correction = hc.detectError(message_str, r)
            end_detection = time.time()
            detection_times.append(end_detection - start_detection)
            print("array de bits con hamming sin error: ", array_hamming.pop())
            # Determine the positions of Redundant Bi
            start = time.time()
            arr = hc.posRedundantBits(message_str, r)
            # Determine the parity bits
            arr = hc.calcParityBits(arr, r)
            end = time.time()
            paritybits_time.append(end-start)
            print("array de bits con hamming con error: ", arr)
            print("La posicion del error es " + str(correction) + "\n")
            print("tiempo promedio para formar los parity bits: ", (sum(paritybits_time))/len(paritybits_time))
            print("tiempo promedio para deteccion del error: ", (sum(detection_times))/len(detection_times))
        else:
            print("no reconocido tipo de mensaje")

    return ascii_string

def capa_decodificacion(current_connection, header):
    """ esta funcion se encarga de decodificar el mensaje para retornar un diccionario"""
    message_length  = int(header.decode('utf-8').strip())
    data = pickle.loads(current_connection.recv(message_length))
    return {"header": header, "data": data}

def listen():
    bandera = True
    while bandera:
        current_connection, address = connection.accept()
        while True:
            try:
                #------------ CAPA DE TRANSMISION ------------
                data = current_connection.recv(HEADER_LENGTH)
                # --------------------------------------------

                msgtrans = capa_decodificacion(current_connection, data)
                #------------ CAPA DE APLICACION ------------
                print("\n-------------> cantidad de bits transferidos: ", msgtrans['data']['bits'])
                print("mensaje tipo: ", msgtrans['data']['type'])
                msgdecode = capa_verificacion(msgtrans)
                print("se recibe: ", msgdecode)
                print("-----------------------------------------------")
                #print("el checksum es " + msgtrans['data']['checksum'])




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
