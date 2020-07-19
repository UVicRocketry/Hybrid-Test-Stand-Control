#TEST STAND

import socket

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((socket.gethostbyname('localhost'), 1234))
s.listen(5)

#Here we read a file to get some test text.
textFile = open("sendText.txt", "r")

clientSocket, address = s.accept()
print("Connection to client established.") #not displaying address??

msg = "Connection to server established"
msg = f"{len(msg):<{HEADERSIZE}}" + msg
clientSocket.send(bytes((msg), "utf-8"))

for x in textFile:
    #clientSocket, address = s.accept()

    msg = x
    msg = f"{len(msg):<{HEADERSIZE}}" + msg

    clientSocket.send(bytes((msg), "utf-8"))

    sleep(1000)

if msg == "":
    clientSocket.close()
