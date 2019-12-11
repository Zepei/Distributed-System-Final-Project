import socket
import ssl
from threading import Thread

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

    ACCEPT_THREAD = Thread(target=accept_incoming_connections, args=(bindsocket, context,))
    ACCEPT_THREAD.start()


def accept_incoming_connections(bindsocket, context):
    while True:
        newsocket, fromaddr = bindsocket.accept()
        connstream = context.wrap_socket(newsocket, server_side=True)
        try:
            Thread(target=deal_with_client, args=(connstream,)).start()
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
    print('did something')


def check_alive():
    print('check alive')