#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
import ping

BUFSIZ = 1024
match_socket = ''
alive_socket = ''


def cheat():
    print('You want to cheat')


def play():
    print("you played")


def start_match():
    match_socket, alive_socket = ping.ping_server('')


table_example_text= 'Heart 10; Space 13; Square 5'
hand_example_text= 'Space Ace; Square five;'

top = tkinter.Tk()
top.title("The Game You Can't Cheat")
main = tkinter.Frame(top)
main.pack()

left_frame = tkinter.Frame(main)
left_frame.pack(side='left')
match_button = tkinter.Button(left_frame, text='Match!', highlightbackground='#3E4149', command=start_match)
match_button.pack()

right_frame = tkinter.Frame(main)
right_frame.pack(side='right')
info_frame = tkinter.Frame(right_frame)
info_frame.pack()
tkinter.Label(info_frame, text='You are player 1234').grid(row=0, column=0)
tkinter.Label(info_frame, text="Any prompts show here: ").grid(row=1, column=0)
table_frame = tkinter.Frame(right_frame)
table_frame.pack()
tkinter.Label(table_frame, text='On the table: ').grid(row=0,column=0)
tkinter.Label(table_frame, text=table_example_text).grid(row=0, column=1)
hand_frame = tkinter.Frame(right_frame)
hand_frame.pack()
tkinter.Label(hand_frame, text='In your hand: ').grid(row=1, column=0)
tkinter.Label(hand_frame, text=hand_example_text).grid(row=1, column=1)
operation_frame = tkinter.Frame(right_frame)
operation_frame.pack()
suit = tkinter.StringVar()
suit.set("enter a suit")
number = tkinter.StringVar()
number.set("enter a number")
suit_field = tkinter.Entry(operation_frame, textvariable=suit)
suit_field.grid(row=0, column=0)
number_field = tkinter.Entry(operation_frame, textvariable=number)
number_field.grid(row=1, column=0)
play_button = tkinter.Button(operation_frame, text="Play!", command=play, highlightbackground='#3E4149')
play_button.grid(row=0, column=1)
cheat_button = tkinter.Button(operation_frame, text="Cheat!", command=cheat, highlightbackground='#3E4149')
cheat_button.grid(row=1, column=1)


# Starts GUI execution.
tkinter.mainloop()
