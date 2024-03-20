import socket
import threading

# Connections
# Requesting Servers IP address and Port Number for User attempting to join the server
host_address = input("Enter Server's Ip Address: ")
# '127.0.0.1'
port_number = int(input("Enter The Server's Port Number: "))
# 3333

# Client's Connection To The Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host_address, port_number))

# To Enter Client's Username
User_name = input("Enter the User Name: ")


def cli_rec():

    while True:
        try:
            # To Receive The Message Sent From The Server
            ser_msg = client.recv(1024).decode('ascii')

            # If Server Sends a Message 'SECRET' Then send the username
            if ser_msg == 'SECRET':
                client.send(User_name.encode('ascii'))

            # When you receive the confirmation from Server
            # to disconnect
            elif ser_msg == "close":
                client.close()
                print("Disconnected from the server!")
                return
            else:
                print(ser_msg)

        except Exception as e:
            # The Connection is closed when there is an Error
            print("Error:", e)
            client.close()
            break


def cli_write():
    while True:
        write_msg = '{}: {}'.format(User_name, input(''))
        client.send(bytes(write_msg, 'ascii'))
        if "quit" in write_msg:
            break


# Start the Threads to Listen And Write
rec_thread = threading.Thread(target=cli_rec)
rec_thread.start()

wr_thread = threading.Thread(target=cli_write)
wr_thread.start()

rec_thread.join()
wr_thread.join()
