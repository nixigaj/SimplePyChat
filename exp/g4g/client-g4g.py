# Import socket module
import socket

# Create a socket object
main_socket = socket.socket()

# socket refresh fix
main_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Define the port on which you want to connect
port = 12345

# connect to the server on local computer
main_socket.connect(('127.0.0.1', port))

# receive data from the server and decoding to get the string.
print(main_socket.recv(1024).decode())
# close the connection
main_socket.close()

# fileio
# select
