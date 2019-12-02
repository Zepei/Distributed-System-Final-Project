#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter

hands = []


class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()


def cheat():
    print('You want to cheat')


def play():
    print("you played")


top = tkinter.Tk()
top.title("The Game You Can't Cheat")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=10, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

hand_frame = tkinter.Frame(top)


entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send, highlightbackground='#3E4149')
send_button.pack()

suit = tkinter.StringVar()
suit.set("enter a suit")
number = tkinter.StringVar()
number.set("enter a number")
suit_field = tkinter.Entry(top, textvariable=suit)
suit_field.pack()
number_field = tkinter.Entry(top, textvariable=number)
number_field.pack()
play_button = tkinter.Button(top, text="Play!", command=play, highlightbackground='#3E4149')
play_button.pack()
cheat_button = tkinter.Button(top, text="Cheat!", command=cheat, highlightbackground='#3E4149')
cheat_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#----Now comes the sockets part----
HOST = input('Enter host(leave blank if not known): ')
if not HOST:
    HOST = "ec2-3-91-101-44.compute-1.amazonaws.com"
else: HOST = ''

PORT = input('Enter port(leave blank if not known): ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.