from socket import *

# server configuration
SERVER_HOST = '127.0.0.1'
SERVER_PORT_UDP = 5555

# dictionary to store clients nicknames and addresses
clients = {}

# handle client registration
def handle_registration(client_address, message):
    nickname = message.split()[1]
    clients[nickname] = client_address
    print(f"New user registered: {nickname}")

# handle direct messages
def handle_message(client_address, message, server_socket):
    parts = message[5:].split(':', 1)
    if len(parts) != 2:
        return "Invalid message format. Use '<recipient>:<message>'."
    
    recipient = parts[0]
    content = parts[1]
    
    # check if recipient exists in clients dictionary
    if recipient in clients:
        recipient_address = clients[recipient]
        # send message to recipient
        server_socket.sendto(f"{get_nickname(client_address)}: {content}".encode(), recipient_address)
    else:
        return "User not found."

# handle broadcast messages
def handle_message_all(client_address, message, server_socket):
    parts = message[8:].split(':', 1)
    if len(parts) != 1:
        return "Invalid message format. Use '<message>'."
    
    content = parts[0]

     # send message to all registered users
    for nickname, recipient_address in clients.items():
        server_socket.sendto(f"{get_nickname(client_address)}: {content}".encode(), recipient_address)

# get nickname of a client
def get_nickname(client_socket):
    for nickname, socket in clients.items():
        if socket == client_socket:
            return nickname
    return "Unknown"

def main():
    # create UDP socket
    server_socket = socket(AF_INET, SOCK_DGRAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT_UDP))
    print(f"Server listening on {SERVER_HOST}:{SERVER_PORT_UDP}")

    while True:
        # receive data and client address
        data, client_address = server_socket.recvfrom(2048)
        message = data.decode()
        print(f"{get_nickname(client_address)}:", message)
        
        response = None
        # process message based on command prefix
        if message.startswith("/REG"):
            handle_registration(client_address, message)
        elif message.startswith("/MSGALL"):
            response = handle_message_all(client_address, message, server_socket)
        elif message.startswith("/MSG"):
            response = handle_message(client_address, message, server_socket)
        
        # send response to client if exists
        if response:
            server_socket.sendto(response.encode(), client_address)

if __name__ == "__main__":
    main()
