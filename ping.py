import socket
import ssl
from threading import Thread
from datetime import datetime

clients = []

def ping_server(CALocation):
    hostname = 'ec2-3-91-101-44.compute-1.amazonaws.com'
    port = 33000
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    context.load_verify_locations(CALocation)
    conn = context.wrap_socket(sock)
    conn.connect(hostname, port)
    return conn


def run_server(certfile, keyfile):
    context = ssl.create_default_context((ssl.Purpose.CLIENT_AUTH))
    context.load_cert_chain(certfile=certfile, keyfile=keyfile)

    bindsocket = socket.socket()
    bindsocket.bind(('ec2-3-91-101-44.compute-1.amazonaws.com', 33000))
    bindsocket.listen(5)

    Thread(target=accept_incoming_connections, args=(bindsocket, context,)).start()


def accept_incoming_connections(bindsocket, context):
    while True:
        if len(clients) == 4:
            continue

        newsocket, fromaddr = bindsocket.accept()
        connstream = context.wrap_socket(newsocket, server_side=True)
        try:
            Thread(target=deal_with_client, args=(connstream,)).start()
            clients.append({"connstream": connstream, "fromaddr": fromaddr})
            if len(clients) == 4:
                broadcast_peers_info(clients)
                ## clear_clients(clients)
        finally:
            connstream.shutdown(socket.SHUT_RDWR)
            connstream.close()


def deal_with_client(connstream):
    data = connstream.recv(1024)
    while data:
        if not do_something(connstream, data):
            break
        data = connstream.recv(1024)


def do_something(connstream, data):
    data = data.decode('UTF-8')
    # handle socket close
    if data == '':
        connstream.close()
        for i in range(len(clients)):
            if clients[i]["connstream"] == connstream:
                del clients[i]
                break
    # handle check_alive response


def broadcast_peers_info(clients):
    for i in range(4):
        if i == 0:
            clients[i]["connstream"].send((clients[1]["fromaddr"]+" "+clients[2]["fromaddr"]+" "+clients[3]["fromaddr"]).encode('UTF-8'))
        if i == 1:
            clients[i]["connstream"].send((clients[2]["fromaddr"]+" "+clients[3]["fromaddr"]).encode('UTF-8'))
        if i == 2:
            clients[i]["connstream"].send((clients[3]["fromaddr"]).encode('UTF-8'))


def clear_clients(clients):
    del clients[:]


def check_alive(clients):
    # check if clients are alive
    # send peers a specific message and expect get right reply in a timely manner
    for client in clients:
        client["connstream"].send(("alive?"+"time="+datetime.utcnow()).encode('UTF-8'))