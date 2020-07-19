#MISSION CONTROL

import socket

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostbyname('localhost'), 1234))

#Here we open a file to write to so we can show the text that has been recieved.

while True:
    textMsg = ''
    newMsg = True
    fullMsg = ''

    while True:
        msg = s.recv(128) # = Bytes which can be recieved at one time
        if newMsg:
            print("new msg len: ", msg[:HEADERSIZE]
            msglen = int(msg[:HEADERSIZE])
            newMsg = False

        print(f"full message length: {msglen}")

        fullMsg += msg.decode("utf-8")

        print(len(fullMsg))

        if (len(fullMsg))-HEADERSIZE == msglen:
            print("full msg recieved")
            print(fullMsg[HEADERSIZE:])
            newMsg = True

        if len(msg) <= 0:
            break
