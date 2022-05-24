import socket #  manejo de conexiones
import errno # manejo de errores
import sys # manejo de sistema

HEAD_LENGHT = 10 # longitud maxima del mensaje
IP = input("IP del servidor: ") # direccion IP del servidor
PORT = int(input("Puerto de la conexión: ")) # puerto de conexion del servidor
my_username = input("Escriba su nombre: ") # nombre del cliente

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creacion del socket tipo internet
client_socket.connect((IP, PORT)) # conexion del socket con la direccion IP y el puerto
client_socket.setblocking(False) # deshabilita el bloqueo de la conexion

username = my_username.encode('utf-8') # codifica el nombre del cliente
username_header = f"{len(username):<{HEAD_LENGHT}}".encode('utf-8') # codifica la cabecera del nombre del cliente
client_socket.send(username_header + username) # envia el nombre del cliente

while True: # ciclo infinito
    message = input(f"{my_username} > ") # ingresa el nomnbre del cliente
    if message: # si hay mensaje
        salir = message #guarda mensaje en salir
        message = message.encode('utf-8') # codifica el mensaje
        message_header = f"{len(message):<{HEAD_LENGHT}}".encode('utf-8') # codifica la cabecera del mensaje
        client_socket.send(message_header + message) # envia el mensaje
        if salir == "chao": # si el mensaje es chao
                print("Desconexión del servidor")
                sys.exit() # cierra el programa

    try: # intenta
        while True:
            #ciclo infinito para recibir mensajes
            username_header = client_socket.recv(HEAD_LENGHT) # recibe la cabecera del nombre del cliente
            if not len(username_header): # si no hay cabecera
                print("Servidor desconectado")
                sys.exit() # cierra el programa
            username_length = int(username_header.decode('utf-8').strip()) # decodifica la cabecera del nombre del cliente
            username = client_socket.recv(username_length).decode('utf-8') # recibe el nombre del cliente
            message_header = client_socket.recv(HEAD_LENGHT) # recibe la cabecera del mensaje
            message_length = int(message_header.decode('utf-8').strip()) # decodifica la cabecera del mensaje y la convierte en entero
            message = client_socket.recv(message_length).decode('utf-8') # recibe el mensaje
            print(f"{username} > {message}") # imprime el mensaje del cliente

    except IOError as e: # manejo de errores
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK: # si el error no es de tipo EAGAIN o EWOULDBLOCK
            print('Error de lectura', str(e)) # imprime el error
            sys.exit() # cierra el programa
        continue # continua el ciclo

    except Exception as e: # manejo de errores
        print('Error General', str(e)) # imprime el error
        pass # continua el ciclo