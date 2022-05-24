import socket
import select

HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server_socket.bind((IP, PORT))
server_socket.listen()
print("Servidor Iniciado y contestado OK")
print("Esperando conexiones...")
socket_list = [server_socket]
clientes={}

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)
        if not len(message_header):
            return False
        message_length = int(message_header.decode('utf-8').strip())
        return {"header": message_header, "data": client_socket.recv(message_length)}
    except:
        return False

while True:
    read_sockets, _, exception_sockets = select.select(socket_list, [], socket_list)
    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            user = receive_message(client_socket)
            if user is False:
                continue
            socket_list.append(client_socket)
            clientes[client_socket] = user
            print(f"Usuario: {clientes[client_socket]['data'].decode('utf-8')} conectado")
        else:
            message = receive_message(notified_socket)
            if message is False:
                print(f"Usuario: {clientes[notified_socket]['data'].decode('utf-8')} abandonó")
                socket_list.remove(notified_socket)
                del clientes[notified_socket]
                continue
            user = clientes[notified_socket]
            for client_socket in clientes:
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
    for notified_socket in exception_sockets:
        socket_list.remove(notified_socket)
        del clientes[notified_socket]