#!/usr/bin/python3

# SPDX-License-Identifier: MIT
# Copyright (c) 2022 Erik Junsved and Johan Raab

import random
import socket
import string
import sys
import threading

DEFAULT_PORT = 22424
DEFAULT_IP = 'a.erix.dev'
DEFAULT_USERNAME = 'user-' + \
                   ''.join(random.choice(string.ascii_lowercase) for _ in range(4))

# Required global variables because this is not OOP yet.
tcp_port: int
client_socket: socket
client_username: str
server_ip: str


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

    msg = f"{client_username}: {input()}"
    try:
        client_socket.send(msg.encode())
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

    socketV4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socketV6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

    try:
        try:
            socketV4.connect((server_ip, tcp_port))
            client_socket = socketV4
        except socket.gaierror:
            try:
                socketV6.connect((server_ip, tcp_port))
                client_socket = socketV6
            except socket.gaierror as e:
                print(f"Failed to connect: {e}")
                setup_server_address()
                setup_client_socket()
                return
    except OverflowError:
        print("Port is outside range. Port must be 0-65535")
        setup_client_socket()
        return


def setup_username():
    global client_username
    client_username = DEFAULT_USERNAME

    username_string = input(f"Enter username [{DEFAULT_USERNAME}]: ")
    if username_string != "":
        client_username = username_string


def cleanup():
    try:
        client_socket.close()
    except NameError:
        pass


def setup_server_address():
    global server_ip
    server_ip = DEFAULT_IP

    address_string = input(f"Enter server address [{DEFAULT_IP}]: ")
    if address_string != "":
        server_ip = address_string


def main():
    try:
        setup_server_address()
        setup_client_socket()
        setup_username()
        threading.Thread(target=client_recv, daemon=True).start()
        while True:
            client_send()

    except (KeyboardInterrupt, SystemExit):
        print('\nReceived keyboard interrupt. Quitting.')
        cleanup()


if __name__ == "__main__":
    main()
