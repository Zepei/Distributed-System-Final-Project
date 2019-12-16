import asyncio
import ssl
import time
import socket

# server global
match_server = None  # the match server
match_clients_addrs = []  # addresses of clients connected to the match server
match_clients_sockets = []  # sockets, no direct manipulation on them
match_clients_writers = []  # the writers to clients
broadcasted = False  # indicate if peer info has been send to clients before
last_alive_time_stamp = []  # last time the serve check alive

# client global
my_position = 0  # this client's position in the game: 0,1,2,3
peer_writers_outgoing = []  # list of writers of all peers that this client instantiated connections to, outgoing connection
peer_writers_incoming = []  # list of writers of all peer connections incoming
peer_addrs = []  # peers address of all 4 clients


# client side code
def ping_server(calocation):
    asyncio.run(start_client(calocation))


async def start_client(calocation):
    # connection to server
    match_hostname = 'ec2-3-91-101-44.compute-1.amazonaws.com'
    match_port = 33000
    match_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    match_context.load_verify_locations(calocation)
    reader, writer = await asyncio.open_connection(match_hostname, match_port, ssl=match_context, family=socket.AF_INET)

    # start a server listening to incoming connections from peers
    peer_server = await asyncio.start_server(peer_server_handle_connection, '', 35000, familiy=socket.AF_INET)
    async with peer_server:
        await peer_server.serve_forever()

    # handle communication to the match server
    while True:
        data = await reader.read(100)
        if not data:
            break
        message = data.decode()
        # if check alive, response current time
        if message.find('alive?'):
            writer.write(('alive!time='+str(time.time())).encode())
            await writer.drain()
        # if peerinfo is received, start connecting peers
        if message.find('peerinfo!'):
            connect_peers(message)
    writer.close()


# the callback that handles incoming peer connections
async def peer_server_handle_connection(reader, writer):
    global peer_writers_incoming
    # record all the writers
    peer_writers_incoming.append(writer)
    while True:
        data = await reader.read(100)
        if not data:
            break
        message = data.decode()


# according to peerinfo, connect peers
def connect_peers(peerinfo):
    global peer_addrs
    global my_position
    # get addresses from all four peers
    # peerinfo has such format: 1peerinfo!123.123.123.12:12345,123.123.123.12:12345,123.123.123.12:12345,123.123.123.12:12345
    peer_addrs = peerinfo[peerinfo.find('!')+1:].split(',')
    # the first digit decide when player this client is
    if peerinfo[0] == '0':
        my_position = 0
        asyncio.run(a_player_connect())
    if peerinfo[0] == '1':
        my_position = 1
        asyncio.run(b_player_connect())
    if peerinfo[0] == '2':
        my_position = 2
        asyncio.run(c_player_connect())
    if peerinfo[0] == '3':
        my_position = 3


# a player connects to b, c, d
async def a_player_connect():
    global peer_addrs
    global peer_writers_outgoing
    b_hostname = peer_addrs[1].split(':')[0]
    b_port = peer_addrs[1].split(':')[1]
    b_reader, b_writer = await asyncio.open_connection(b_hostname, 35000, family=socket.AF_INET)
    peer_writers_outgoing.append(b_writer)

    c_hostname = peer_addrs[2].split(':')[0]
    c_port = peer_addrs[2].split(':')[1]
    c_reader, c_writer = await asyncio.open_connection(c_hostname, 35000, family=socket.AF_INET)
    peer_writers_outgoing.append(c_writer)

    d_hostname = peer_addrs[3].split(':')[0]
    d_port = peer_addrs[3].split(':')[1]
    d_reader, d_writer = await asyncio.open_connection(d_hostname, 35000, family=socket.AF_INET)
    peer_writers_outgoing.append(d_writer)


# b player connects to c, d
async def b_player_connect():
    global peer_addrs
    c_hostname = peer_addrs[2].split(':')[0]
    c_port = peer_addrs[2].split(':')[1]
    c_reader, c_writer = await asyncio.open_connection(c_hostname, 35000, family=socket.AF_INET)
    peer_writers_outgoing.append(c_writer)

    d_hostname = peer_addrs[3].split(':')[0]
    d_port = peer_addrs[3].split(':')[1]
    d_reader, d_writer = await asyncio.open_connection(d_hostname, 35000, family=socket.AF_INET)
    peer_writers_outgoing.append(d_writer)


# c player connects to d
async def c_player_connect():
    global peer_addrs
    d_hostname = peer_addrs[3].split(':')[0]
    d_port = peer_addrs[3].split(':')[1]
    d_reader, d_writer = await asyncio.open_connection(d_hostname, 35000, family=socket.AF_INET)
    peer_writers_outgoing.append(d_writer)


# server side code
def run_server(certfile, keyfile):
    asyncio.run(start_server(certfile, keyfile))


async def start_server(certfile, keyfile):
    global match_server
    match_hostname = 'ec2-3-91-101-44.compute-1.amazonaws.com'
    match_port = 33000
    match_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    match_context.load_cert_chain(certfile=certfile, keyfile=keyfile)
    match_server = await asyncio.start_server(match_handle_connection, match_hostname, match_port, ssl=match_context, familiy=socket.AF_INET)
    async with match_server:
        await match_server.serve_forever()

    # check alive every 30 seconds
    loop = asyncio.get_event_loop()
    loop.call_later(30, check_alive, loop)


async def match_handle_connection(reader, writer):
    global match_server
    global match_clients_addrs
    global match_clients_sockets
    global match_clients_writers
    global broadcasted
    global last_alive_time_stamp
    # if 5th connections comes, reject
    if len(match_clients_addrs > 4) or len(match_clients_sockets > 4):
        writer.close()
        return

    # update globals
    addr = writer.get_extra_info('peername')
    match_clients_addrs.append(addr)
    match_clients_sockets = match_server.sockets
    match_clients_writers.append(writer)
    last_alive_time_stamp[str(addr)] = 0
    # if have 4 connections, broadcast peerinfo
    if len(match_clients_addrs) == 4 and len(match_clients_sockets) == 4:
        if not broadcasted:
            writer_index = match_clients_writers.index(writer)
            message = (writer_index+'peerinfo!'+match_clients_addrs[0]+','+match_clients_addrs[1]+','+match_clients_addrs[2]+','+match_clients_addrs[3]).encode()
            for a_writer in match_clients_writers:
                a_writer.write(message)
                await writer.drain()
            broadcasted = True

    while True:
        data = await reader.read(100)
        if not data:
            break
        message = data.decode()
        # check alive here, assume response is like alive!time=123456789
        if message.find('alive!'):
            response_time = message[message.find('=')+1:]
            last_alive_time_stamp[str(addr)] = int(response_time)

    # close this socket
    match_clients_addrs.remove(addr)
    match_clients_writers.remove(writer)
    writer.close()
    match_clients_sockets = match_server.sockets
    if len(match_clients_addrs != 4) and len(match_clients_sockets != 4):
        broadcasted = False


async def check_alive(loop):
    global match_clients_writers
    global last_alive_time_stamp
    global match_clients_addrs
    global match_clients_sockets
    global match_server
    now = time.time()

    for writer in match_clients_writers:
        addr = writer.get_extra_info('peername')
        if int(now) - last_alive_time_stamp[str(addr)] > 20:
            # this connection is lost
            match_clients_addrs.remove(addr)
            match_clients_writers.remove(writer)
            writer.close()
            match_clients_sockets = match_server.sockets

    for writer in match_clients_writers:
        writer.write("alive?")
        await writer.drain()
    loop.call_later(30, check_alive, loop)
