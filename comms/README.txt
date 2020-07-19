This is the communications system to relay information between
the engine on the test stand and mission control.


Server Requirements
 - Initiate a socket
 - Establish a connection with client through socket
 - Time out if no message received for 30 secs
 - Send single lines of data at 100Hz
 - Receive commands at 100Hz opposite from data
 - Read data from file and ONLY send at 100Hz current data
 - Print commands to file

Client Requirements
 - Connect to server socket
 - Receive data at 100Hz
 - Send commands at 100Hz opposite from data
 - Print data to file
 - Read commands from file at 100Hz
 - Safely tell both server and client to disconnect from socket

Communications Protocol
 - Whatever is decided for encoding purposes

While communication is held, repeat:
 - Send data
 - Wait 5 milliseconds
 - Send commands
 - Wait 5 milliseconds
