import socket
import threading
import time
import datetime

nicknames = []

def handle_client(client_socket, client_address, nickname_to_socket,nickname):
    # This function will handle incoming messages from the client
    # and broadcast them to all other clients
    nicknames.append(nickname)

    client_socket.send(f'(Server) Welcome {nickname}, there are {len(nicknames)} user(s): {", ".join(nicknames)}'.encode("utf-8"))
    print(f"{nickname} Connected at {time.ctime()}")
    # broadcast(f"{nickname} has joined the chat.", nickname_to_socket)

    while True:
        message = client_socket.recv(1024).decode("utf-8")
        if message == "QUIT":
            client_socket.close()
            del nickname_to_socket[nickname]
            nicknames.remove(nickname)
            serv_strt = "(Server) " 
            broadcast(f'{ serv_strt +nickname} Disconnected, there are {len(nicknames)} user(s): {", ".join(nicknames)}',nickname_to_socket,nickname)
            break
        elif message == "LIST":
            client_socket.send(f'(Server) Active users : {", ".join(nicknames)}'.encode("utf-8"))
        else:
            with open("log.txt", "a") as file:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write(f"{timestamp}: {nickname}: {message}\n")

            broadcast(f"{'('+nickname+') '+message}", nickname_to_socket,nickname)
    print(f"{nickname} Disconnected at {time.ctime()}")

def broadcast(message, nickname_to_socket,sender_nickname):
    # This function broadcasts a message to all clients

    for nickname, socket in nickname_to_socket.items():
        if nickname != sender_nickname:
            socket.send(message.encode("utf-8"))
def start_server(port):
    # This function starts the server
    print("Server started at", time.ctime(), "waiting for connections…")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen()
    nickname_to_socket = {}
    while True:
        client_socket, client_address = server_socket.accept()
        nickname = client_socket.recv(1024).decode("utf-8")
        nickname_to_socket[nickname] = client_socket
        broadcast(f"{'(Server) '+nickname} joining now",nickname_to_socket,nickname)
        client_thread = threading.Thread(
            target=handle_client,
            args=(client_socket, client_address, nickname_to_socket,nickname),
        )
        client_thread.start()


if __name__ == '__main__':
    start_server(8000)