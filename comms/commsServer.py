#TEST STAND

import socket

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((socket.gethostbyname('localhost'), 1234))
s.listen(5)

while True:
    clientSocket, address = s.accept()
    print(f"Connection from {address} has been established.") #not displaying address??

    msg = "Welcome to the server!"
    msg = f"{len(msg):<{HEADERSIZE}}" + msg

    clientSocket.send(bytes((msg), "utf-8"))
    clientSocket.close()
