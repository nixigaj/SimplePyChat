import socket
import string
import sys
import threading
import random

DEFAULT_PORT = 13377
DEFAULT_IP = 'nixivps'
DEFAULT_USERNAME = 'user-' + \
                   ''.join(random.choice(string.ascii_lowercase) for _ in range(4))

# Required global variables because this is not OOP yet.
tcp_port: int
client_socket: socket


def client_recv():
    while True:
        msg = client_socket.recv(1024).decode()
        if msg:
            if msg == '$SERVER_CLOSED':
                print("Server closed. Press enter or ctrl+c to quit.")
                client_socket.close()
                sys.exit(0)
            print(msg)
        else:
            print("Server socket closed. Press enter or ctrl+c to quit.")
            client_socket.close()
            sys.exit(0)


def client_send():
    global client_socket

    msg = f"{DEFAULT_USERNAME}: {input()}"
    try:
        client_socket.sendall(msg.encode())
    except OSError:
        sys.exit(0)


def setup_client_socket():
    global tcp_port
    tcp_port = DEFAULT_PORT
    global client_socket

    try:
        tcp_port_string = input(f"Enter connection port [{DEFAULT_PORT}]: ")
        if tcp_port_string != "":
            tcp_port = int(tcp_port_string)
    except ValueError:
        print("Not a valid port. Please enter an integer.")
        setup_client_socket()
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((DEFAULT_IP, tcp_port))
    except OverflowError:
        print("Port is outside range. Port must be 0-65535")
        setup_client_socket()
        return


def cleanup():
    try:
        client_socket.close()
    except NameError:
        pass


def main():
    try:
        setup_client_socket()
        threading.Thread(target=client_recv, daemon=True).start()
        while True:
            client_send()

    except (KeyboardInterrupt, SystemExit):
        print('\nReceived keyboard interrupt. Quitting.')
        cleanup()


if __name__ == "__main__":
    main()
