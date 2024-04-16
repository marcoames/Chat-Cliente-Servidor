from socket import *

# OPERACOES
#/REG registra cliente
#/MSG <destino>:<mensagem>
#/MSGALL <mensagem>
#/FILE <destino>:<arquivo.txt>

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5555

def register_user(client_socket, nickname):
    client_socket.send(f"/REG {nickname}".encode())

def send_message(client_socket, recipient, message):
    #print(f"/MSG {recipient}:{message}")
    client_socket.send(f"/MSG {recipient}:{message}".encode())

def send_to_all(client_socket, message):
    client_socket.send(f"/MSGALL {message}".encode())

def main():
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    #registra usuario
    command = input("Enter:")
    if command.startswith('/REG'):
        register_user(client_socket, command[5:])  # Exclude '/REG ' from the message
    else:
        print("You need to register a new user using '/REG <nickname>'.")
        client_socket.close()
        return
    
    # Set the socket to non-blocking mode
    client_socket.setblocking(False)

    while True:
        
        # VERIFICA SE TEM MENSAGEM PARA IMPRIMIR
        try:
            # Try to receive data from the server
            decoded_message = client_socket.recv(2048).decode()
            if decoded_message:
                print(decoded_message)  # Print the received message from the server
            else:
                print("Connection closed by server.")
                client_socket.close()
                exit()  

        except BlockingIOError:
            pass  # No data available, continue loop   

        command = input("Enter: ").strip()

        if command.startswith('/REG'):
            register_user(client_socket, command[5:])  # Exclude '/REG ' from the message
        elif command.startswith('/MSGALL'):
            message = command[8:].strip() # Exclude '/MSGALL' from message
            send_to_all(client_socket, message)
        elif command.startswith('/MSG'):
            parts = command[5:].split(':',1) #Exclude '/MSG' from message
            if len(parts) != 2:
                print("Invalid command format. Use '/MSG <recipient>:<message>'.")
                continue
            #print(parts)
            recipient, message = parts[0], parts[1]
            send_message(client_socket, recipient, message)
        elif command.startswith('/FILE'):
            parts = command[6:].split(':',1) #Exclude '/MSG' from message
            recipient = parts[0]
            file_path = parts[1]
            try:
                with open(file_path, "r") as file:
                    message = file.read()
            except FileNotFoundError:
                print("File not found or cannot be opened.")
                break
            send_message(client_socket, recipient, message)
        elif command == "":
            pass
        elif command == "EXIT":
            break
        else:
            print("Invalid command.")

    client_socket.close()
     #####################

        


                
if __name__ == "__main__":
    main()
