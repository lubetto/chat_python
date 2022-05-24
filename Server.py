import socket #  manejo de conexiones
import select # manejo I/O multiple

HEADER_LENGTH = 10 # longitud maxima del mensaje
IP = "127.0.0.1" # direccion IP del servidor
PORT = 8080 # puerto de conexion del servidor

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creacion del socket tipo internet
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reutilizacion de la direccion IP y el puerto para permitir mas conexiones

server_socket.bind((IP, PORT)) # conexion del socket con la direccion IP y el puerto
server_socket.listen() # escucha de conexiones
print("Servidor Iniciado y contestado OK")
print("Esperando conexiones...")
socket_list = [server_socket] # lista de sockets a escuchar
clientes={} # diccionario de clientes

def receive_message(client_socket): # funcion para recibir mensajes
    try:
        message_header = client_socket.recv(HEADER_LENGTH) # recibe el mensaje del cliente
        if not len(message_header): # si no hay mensaje
            return False # termina la funcion
        message_length = int(message_header.decode('utf-8').strip()) # convierte la cabecera del mensaje a entero
        return {"header": message_header, "data": client_socket.recv(message_length)} # retorna el mensaje
    except:
        return False

while True: # ciclo infinito
    read_sockets, _, exception_sockets = select.select(socket_list, [], socket_list) # selecciona los sockets a leer
    for notified_socket in read_sockets: # recorre los sockets a leer
        if notified_socket == server_socket: # si el socket es el servidor
            client_socket, client_address = server_socket.accept() # acepta la conexion del cliente
            user = receive_message(client_socket) # recibe el mensaje del cliente
            if user is False: # si no hay mensaje
                continue # continua el ciclo
            socket_list.append(client_socket) # agrega el socket a la lista de sockets a escuchar
            clientes[client_socket] = user # agrega el cliente a la lista de clientes
            print(f"Usuario: {clientes[client_socket]['data'].decode('utf-8')} conectado")
        else: # si el socket es un cliente
            message = receive_message(notified_socket) # recibe el mensaje del cliente
            if message is False: # si no hay mensaje
                print(f"Usuario: {clientes[notified_socket]['data'].decode('utf-8')} abandonó") # imprime que el cliente abandono
                socket_list.remove(notified_socket) # remueve el socket de la lista de sockets a escuchar
                del clientes[notified_socket] # remueve el cliente de la lista de clientes
                continue # continua el ciclo
            user = clientes[notified_socket] # obtiene el cliente
            for client_socket in clientes: # recorre los clientes
                if client_socket != notified_socket: # si el cliente no es el mismo que el que notifico
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data']) # envia el mensaje al cliente
    for notified_socket in exception_sockets: # recorre los sockets que generaron excepciones
        socket_list.remove(notified_socket)# remueve el socket de la lista de sockets a escuchar
        del clientes[notified_socket]# remueve el cliente de la lista de clientes