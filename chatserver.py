from collections import defaultdict
from email.policy import default
import socket
import threading

# Server's host address and port number
host_address = '127.0.0.1'
port_number = 3333

# Server start
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host_address, port_number))
server.listen()
print(f'Server Running with Address: {host_address} on Port: {port_number}')

clients = []
user_names = defaultdict(int)


def bc(bc_msg):
    for client in clients:
        client.send(bc_msg)


leftUser = ''

# To Handle Client Messages


def handle_cli_msgs(client):
    global leftUser
    while True:
        try:
            message = client.recv(1024)
            msg = message.decode('ascii')
            msgString = str(msg)
            # print("Message from client", msg)
            # print("usernames:", user_names)
            # dm
            if "/dm" in msg:
                msgContent = msgString.split(" ")
                # print(msgContent)
                sender_name = msgContent[0]
                user_name = msgContent[2]
                sen_msg = " ".join(msgContent[3:])
                sen_msg_rep = sen_msg.replace('"', '')
                # print(sen_msg_rep)
                con_mg = sender_name + sen_msg_rep
                bt_conv = bytes(con_mg, "ascii")
                if user_name in user_names:
                    clients[user_names[user_name]].send(bt_conv)
                    client.send(bt_conv)
                else:
                    client.send(
                        bytes(f"Server: {user_name} is not connected to the server", "ascii"))
            # /bc
            elif "/bc" in msg:
                msgContent = msgString.split(" ")
                # print(msgContent)
                user_name = msgContent[0]
                sen_msg = " ".join(msgContent[2:])
                sen_msg_rep = sen_msg.replace('"', '')
                con_mg = user_name + sen_msg_rep
                bt_conv = bytes(con_mg, "ascii")
                for client in clients:
                    client.send(bt_conv)
            # /help
            elif "/help" in msg:
                __, _ = msgString.split(" ")
                msg_by = bytes("Server:\n/help: This command will print the list of commands and their respective behaviors\n"
                               "/users: This command requests the server and prints the list of connected users to the server.\n"
                               "/dm username 'message': This command is used by client to send the message between quotes to the specified user.\n"
                               "/bc 'message': This command is used by client to send message to all the connected users to the client.\n"
                               "/quit: This command lets the client to disconnect from the server. Before disconnecting from server, a message is sent to server and connect users that client is quitting from the server.", "ascii")
                client.send(msg_by)
            # /users
            elif "/users" in msg:
                # __, _ = msgString.split(" ")
                for key in user_names:
                    client.send(bytes(f"{key}", "ascii"))

            # /quit
            elif "/quit" in msg:
                __, _ = msgString.split(" ")
                client.send(bytes("close", "ascii"))
                capture_ix = clients.index(client)
                clients.remove(client)
                client.close()
                for k, v in user_names.items():
                    if v == capture_ix:
                        leftUser = k
                        print(f'{leftUser} has quit the server')
                        bc(f'Server: {leftUser} has quit the server!'.encode(
                            'ascii'))
                        del user_names[k]
                        break
                break

        except Exception as error:

            capture_ix = clients.index(client)
            clients.remove(client)
            client.close()
            for k, v in user_names.items():
                if v == capture_ix:
                    leftUser = k
                    print(f"{leftUser} has lost the connection")
                    bc(f'Server: {leftUser} has lost the connection!'.encode(
                        'ascii'))
                    del user_names[k]
                    break

            break


def rec_clis():
    while True:
        # Accepting the Connection
        client, cli_add = server.accept()
        print("Connected with {}".format(str(cli_add)))

        client.send('SECRET'.encode('ascii'))
        user_name = client.recv(1024).decode('ascii')

        clients.append(client)
        user_names[user_name] = len(clients) - 1

        print("Username is {}".format(user_name))
        bc("{} has joined the server!".format(user_name).encode('ascii'))
        client.send(
            f"Welcome!\nyou are now connected to server with server's\nAddress: {host_address}\nPort: {port_number}".encode('ascii'))
        # Starting  Thread to handle Client
        thread = threading.Thread(target=handle_cli_msgs, args=(client, ))
        thread.start()


rec_clis()
