from socket import *
import threading

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5555

clients = {}

def handle_client(client_socket, client_address):
    try:
        while True:
            message = client_socket.recv(2048).decode()
            print(message)
            if not message:
                print(f"Connection with {client_address} closed.")
                break
            if message.startswith("/REG"):
                handle_registration(client_socket, message)
            elif message.startswith("/MSGALL"):
                handle_message_all(client_socket,message)
                pass  
            elif message.startswith("/MSG"):
                handle_message(client_socket, message)
            else:
                print(f"Invalid message from {client_address}: {message}")
    except ConnectionResetError:
        print(f"Connection with {client_address} lost.")
    finally:
        client_socket.close()

def handle_registration(client_socket, message):
    nickname = message.split()[1]
    clients[nickname] = client_socket
    print(f"Novo usuário registrado: {nickname}")

def handle_message(sender_socket, message):
    parts = message[5:].split(':',1)
    print(parts)
    if len(parts) != 2:
        sender_socket.send("Formato de mensagem inválido. Use '<destinatário>:<mensagem>'.".encode())
        return
    
    recipient = parts[0]
    content = parts[1]
    
    if recipient in clients:
        recipient_socket = clients[recipient]
        recipient_socket.send(f"{get_nickname(sender_socket)}:{content}".encode())
    else:
        sender_socket.send("Usuário não encontrado.".encode())

def handle_message_all(sender_socket, message):
    parts = message[8:].split(':',1)
    print(parts)
    if len(parts) != 1:
        sender_socket.send("Formato de mensagem inválido. Use '<mensagem>'.".encode())
        return
    
    content = parts[0]
    
    for nickname, recipient_socket in clients.items():
        recipient_socket.send(f"{get_nickname(sender_socket)}: {content}".encode())

def get_nickname(client_socket):
    for nickname, socket in clients.items():
        if socket == client_socket:
            return nickname
    return "Desconhecido"

def main():
    server_socket = socket(AF_INET,SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Nova conexão de {client_address}")
        
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    main()
