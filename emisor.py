import socket
import random
import pickle
from bitarray import bitarray

HEADER_LENGTH = 10
HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 9090  # The port used by the server
bits_transmitidos = 0

def capa_transmision(sock, msg):
	dprotocol = {
		"type":"mensaje_emisor",
		"message": msg
	}
	# serializing dprotocol
	msg = pickle.dumps(dprotocol)
	# adding header to msg
	msg = bytes(f"{len(msg):<{HEADER_LENGTH}}", "utf-8") + msg
	sock.send(msg)
	return True

def capa_ruido(msg_encode):
	#cada 100 bits mandados se le remueve un bit random al mensaje
	len_msg = msg_encode.length()
	global bits_transmitidos
	print("bits transmitidos = ", bits_transmitidos)
	bits_transmitidos= bits_transmitidos + len_msg
	if(bits_transmitidos >= 100):
		msg_encode.pop(random.randint(1,len_msg - 1))
	else:
		return msg_encode

def capa_verificacion(msg):
	#Convertimos el string (msg) a ASCII binario
	ascii_binario = bin(int.from_bytes(msg.encode(), 'big'))
	#Eliminamos el prefijo 0b 
	ascii_binario = ascii_binario[2:]
	#lo convertimos en un bitarray
	bit_array = bitarray(ascii_binario)
	
	return bit_array

def capa_aplicacion():
	bandera = True
	while(bandera):
		msg = input("¿Qué mensaje desea enviar al receptor? ")
		msg_encode = capa_verificacion(msg)
		msg_encode_noise = capa_ruido(msg_encode)
		trans = capa_transmision(client_socket, msg_encode_noise)
		if(trans):
			print("Mensaje enviado con exito")
		else:
			print("Error al enviar el mensaje")

if __name__ == "__main__":
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect((HOST,PORT))
	client_socket.setblocking(False)
	print(f"conectado a servidor {HOST}:{PORT}")
	try:
		capa_aplicacion()
	except KeyboardInterrupt:
		print("Hasta pronto")
		client_socket.shutdown(socket.SHUT_RDWR)
		client_socket.close()