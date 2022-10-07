# first of all import the socket library
import socket

# next create a socket object
main_socket = socket.socket()
print("Socket successfully created")

# socket refresh fix
main_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# reserve a port on your computer in our
# case it is 12345, but it can be anything
port = 12345

# Next bind to the port
# we have not typed any ip in the ip field
# instead we have inputted an empty string
# this makes the server listen to requests
# coming from other computers on the network
main_socket.bind(('', port))
print("socket bound to %s" % port)

# put the socket into listening mode
main_socket.listen(5)
print("socket is listening")

# a forever loop until we interrupt it or
# an error occurs
while True:
    # Establish connection with client.
    c, addr = main_socket.accept()
    print('Got connection from', addr)

    # send a thank-you message to the client. encoding to send byte type.
    c.send('Thank you for connecting'.encode())

    # Close the connection with the client
    c.close()

    # Breaking once connection closed
    break

main_socket.close()
