"""
Universidad del Valle de Guatemala
Redes
Catedrático: Vinicio Paz
Pablo Viana - 16091
Sergio Marchena - 16387
"""

import socket
import random
import pickle
from bitarray import bitarray
import hamming_code as hc

HEADER_LENGTH = 10
HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 9090  # The port used by the server
bits_transmitidos = 0
n = 1
checksumCalculado = "2"

def capa_transmision_con_ruido(sock, msge):
	dprotocol = {
		"type":"mensaje_con_ruido",
		"message": msge,
		"bits": bits_transmitidos,
		"checksum": checksumCalculado
	}
	# serializing dprotocol
	msg = pickle.dumps(dprotocol)
	# adding header to msg
	msg = bytes(f"{len(msg):<{HEADER_LENGTH}}", "utf-8") + msg
	sock.send(msg)
	return True

def capa_transmision_sin_ruido(sock, msge):
	dprotocol = {
		"type":"mensaje_sin_ruido",
		"message": msge,
		"bits": bits_transmitidos,
		"checksum": checksumCalculado
	}
	# serializing dprotocol
	msg = pickle.dumps(dprotocol)
	# adding header to msg
	msg = bytes(f"{len(msg):<{HEADER_LENGTH}}", "utf-8") + msg
	sock.send(msg)
	return True

def capa_ruido(msg_encode):
	#cada 100 bits mandados se le remueve un bit random al mensaje
	msg_encode.pop(random.randint(1,msg_encode.length() - 1))
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
	global bits_transmitidos
	global checksumCalculado
	bandera = True
	while(bandera):
		menu = True
		while(menu):
			msg = input("¿Qué mensaje desea enviar al receptor? ")
			if msg == "":
				print("mensaje vacio")
			else:
				menu = False

		#Aqui tengo el mensaje en bits e.g 101010000100101
		msg_encode = capa_verificacion(msg)
		hola = str(msg_encode)
		checksumCalculado += hola
		#Variable de control
		trans = False

		bits_transmitidos += msg_encode.length()
		if bits_transmitidos > 100:
			trans_free = capa_transmision_sin_ruido(client_socket, msg_encode)
			msg_encode_noise = capa_ruido(msg_encode)
			trans = capa_transmision_con_ruido(client_socket, msg_encode_noise)
			bits_transmitidos = 0
		else:
			trans_free = capa_transmision_sin_ruido(client_socket, msg_encode)

		if(trans or trans_free):
			print("Mensaje enviado con exito")
		else:
			print("Error al enviar el mensaje")
		if msg == 'salir':
			print("Hasta pronto")
			return

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
