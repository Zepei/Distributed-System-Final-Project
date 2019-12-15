import socket
import selectors
import ssl
from threading import Thread, Timer
from datetime import datetime

sel = selectors.DefaultSelector()
clients = []
check_alive_clients = []
check_alive_last_time_stamp = 0

def ping_server(CALocation):
    hostname = 'ec2-3-91-101-44.compute-1.amazonaws.com'

    # match making connection
    match_port = 33000
    match_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    match_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    match_context.load_verify_locations(CALocation)
    match_conn = match_context.wrap_socket(match_sock)

    # check_alive connection
    alive_port = 34000
    alive_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    alive_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    alive_context.load_verify_locations(CALocation)
    alive_conn = alive_context.wrap_socket(alive_sock)

    match_conn.connect(hostname, match_port)
    match_conn.connect(hostname, alive_port)

    return match_conn, alive_conn


def run_server(certfile, keyfile):
    match_context = ssl.create_default_context((ssl.Purpose.CLIENT_AUTH))
    match_context.load_cert_chain(certfile=certfile, keyfile=keyfile)

    alive_context = ssl.create_default_context((ssl.Purpose.CLIENT_AUTH))
    alive_context.load_cert_chain(certfile=certfile, keyfile=keyfile)

    match_socket = socket.socket()
    match_socket.bind('ec2-3-91-101-44.compute-1.amazonaws.com', 33000)
    match_socket.listen(5)
    # match_socket.setblocking(False)
    # sel.register(match_socket, selectors.EVENT_READ, accept_incoming_connections)

    alive_socket = socket.socket()
    alive_socket.bind('ec2-3-91-101-44.compute-1.amazonaws.com', 34000)
    alive_socket.listen(5)
    # alive_socket.setblocking(False)
    # sel.register(alive_socket, selectors.EVENT_READ, alive_accept_incoming_connections)

    Thread(target=accept_incoming_connections, args=(match_socket, match_context,)).start()
    Thread(target=alive_accept_incoming_connections, args=(alive_socket, alive_context,)).start()

    check_alive_interval = Timer(30, check_alive).start()


def alive_accept_incoming_connections(alive_socket, alive_context):
    while True:
        if len(check_alive_clients) == 4:
            continue
        newsocket, fromaddr = alive_socket.accept()
        connstream = alive_context.wrap_socket(newsocket, server_side=True)
        try:
            check_alive_clients.append({"connstream": connstream, "fromaddr": fromaddr, "last_alive_time": int(datetime.utcnow())})
            Thread(target=alive_deal_with_client, args=(connstream,)).start()
        finally:
            for i in range(len(check_alive_clients)):
                if check_alive_clients[i]["connstream"] == connstream:
                    del check_alive_clients[i]
                    break
            connstream.shutdown(socket.SHUT_RDWR)
            connstream.close()


def accept_incoming_connections(match_socket, match_context):
    while True:
        if len(clients) == 4:
            continue
        newsocket, fromaddr = match_socket.accept()
        connstream = match_context.wrap_socket(newsocket, server_side=True)
        try:
            clients.append({"connstream": connstream, "fromaddr": fromaddr})
            Thread(target=deal_with_client, args=(connstream,)).start()
            if len(clients) == 4:
                broadcast_peers_info(clients)
        finally:
            for i in range(len(clients)):
                if clients[i]["connstream"] == connstream:
                    del clients[i]
                    break
            connstream.shutdown(socket.SHUT_RDWR)
            connstream.close()


def alive_deal_with_client(connstream):
    data = connstream.recv(1024)
    while data:
        if not alive_do_something(connstream, data):
            break
        data = connstream.recv(1024)


def deal_with_client(connstream):
    data = connstream.recv(1024)
    while data:
        if not do_something(connstream, data):
            break
        data = connstream.recv(1024)


# assume the response is like 'alive!time=1234567890'
def alive_do_something(connstream, data):
    data = data.decode('UTF-8')
    if data.find('alive!') > 0:
        time = int(data[data.find('=')+1:])
        for i in range(len(check_alive_clients)):
            if check_alive_clients[i]["connstream"] == connstream:
                check_alive_clients[i]["last_alive_time"] = time
                break


def do_something(connstream, data):
    data = data.decode('UTF-8')


def broadcast_peers_info(clients):
    for i in range(4):
        if i == 0:
            clients[i]["connstream"].send((clients[1]["fromaddr"]+" "+clients[2]["fromaddr"]+" "+clients[3]["fromaddr"]).encode('UTF-8'))
        if i == 1:
            clients[i]["connstream"].send((clients[2]["fromaddr"]+" "+clients[3]["fromaddr"]).encode('UTF-8'))
        if i == 2:
            clients[i]["connstream"].send((clients[3]["fromaddr"]).encode('UTF-8'))


def clear_clients():
    del clients[:]
    del check_alive_clients[:]


def check_alive():
    check_alive_last_time_stamp = datetime.utcnow()
    for client in check_alive_clients:
        if check_alive_last_time_stamp - client["last_alive_time"] > 1000000 * 30:
            print("This client is offline: "+client)
            for i in range(len(check_alive_clients)):
                if check_alive_clients[i]["connstream"] == client:
                    check_alive_clients[i]["connstream"].shutdown(socket.SHUT_RDWR)
                    check_alive_clients[i]["connstream"].close()
                    del check_alive_clients[i]
                    break
            for i in range(len(clients)):
                if clients[i]["connstream"] == client:
                    clients[i]["connstream"].shutdow(socket.SHUT_RDWR)
                    clients[i]["connstream"].close()
                    del clients[i]
                    break
    for client in check_alive_clients:
        client["connstream"].send(("alive?" + "time=" + check_alive_last_time_stamp).encode('UTF-8'))
