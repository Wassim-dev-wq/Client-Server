import socket
import threading
import sys


def receive(client_socket,username):
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            print(f"{message}\n({username}) ",end="")
        except:
            print("Disconnect..")
            client_socket.close()
            break

def start_client(host, port, username):
    # This function starts the client
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.send(username.encode("utf-8"))
    print(client_socket.recv(1024).decode())

    # Connect to the new port assigned by the server
    receive_thread = threading.Thread(target=receive, args=(client_socket,username))
    receive_thread.start()
    message = ""
    while True:
        if message == "LIST":
            message = input("")
        else:
            message = input(f"({username}) ")         
        if message == "QUIT":
            client_socket.send(message.encode("utf-8"))
            client_socket.close()
            break
        elif message == "LIST":
            client_socket.send(message.encode("utf-8"))
        else:
            client_socket.send(message.encode("utf-8"))
        

# get local machine name
host = sys.argv[1]                           
port = int(sys.argv[2])
username = sys.argv[3]
start_client(host,port,username)

