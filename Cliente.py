import socket
import errno
import sys

HEAD_LENGHT = 10
IP = input("IP del servidor: ")
PORT = int(input("Puerto de la conexión: "))
my_username = input("Escriba su nombre: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
client_socket.setblocking(False)

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEAD_LENGHT}}".encode('utf-8')
client_socket.send(username_header + username)

while True:
    message = input(f"{my_username} > ")
    if message:
        salir = message
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEAD_LENGHT}}".encode('utf-8')
        client_socket.send(message_header + message)
        if salir == "chao":
                print("Desconexión del servidor")
                sys.exit()

    try:
        while True:
            #ciclo infinito para recibir mensajes
            username_header = client_socket.recv(HEAD_LENGHT)
            if not len(username_header):
                print("Servidor desconectado")
                sys.exit()
            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')
            message_header = client_socket.recv(HEAD_LENGHT)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')
            print(f"{username} > {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Error de lectura', str(e))
            sys.exit()
        continue

    except Exception as e:
        print('Error General', str(e))
        pass