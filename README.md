Final project for IFT 510 Princ of Comp & Info Tech Arch (ASU)

Developed a fully functional Chat Server using the TCP protocol. Utilized multithreading to run multiple clients where each client is considered as a single thread. TCP socket is used to implement the network connection and communication. We have one server, and it should be run first before the clients attempt to connect to the server. The clients must connect to the server using the server’s IP address and port number. Upon successful connection to the server, the clients can communicate with each other. The clients have features like broadcasting their messages to all connected users, direct message to the specific user connected to the server, requesting the list of users connected to theserver, request help to server to know the usage and descriptions of the commands, and quit the server. These features can be utilized by using the specific commands

Commands:
/help: This command will print the list of commands and their respective behaviors.

/users: This command requests the server and prints the list of connected users to the server.

/dm username 'message': This command is used by client to send the message between quotes to the specified user.

/bc 'message': This command is used by client to send message to all the connected users to the client.

/quit: This command lets the client to disconnect from the server. Before disconnecting from server, a message is sent to server and connect users that client is quitting from the server.
