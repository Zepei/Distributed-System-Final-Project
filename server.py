"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

num_of_clients = 0
clients = {}
addresses = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    global num_of_clients
    global clients
    global addresses
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""
    global num_of_clients
    global clients
    global addresses
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the game!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
    num_of_clients += 1
    if num_of_clients == 4:
        broadcast('4 players are ready,')
        game_start()


    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name + ": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            num_of_clients -= 1
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            if num_of_clients != 4:
                game_over()
            break


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    global num_of_clients
    global clients
    global addresses
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


def game_start():
    broadcast('The Game Has Started')


def game_over():
    broadcast("Game Over")


def cheat_detected(cheating_player):
    broadcast("Player %s is trying to cheat!" % cheating_player)
    game_over()


SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()