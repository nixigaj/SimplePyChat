import socket
import threading
import time

DEFAULT_PORT = 13377


class StrFormat:
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'
    END_C = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Required global variables.
tcp_port: int
client_sockets: list[socket]
main_socket: socket


def setup_socket():

    global tcp_port
    tcp_port = DEFAULT_PORT
    global main_socket

    try:
        tcp_port_string = input(f"Enter connection port [{DEFAULT_PORT}]: ")
        if tcp_port_string != "":
            tcp_port = int(tcp_port_string)
    except ValueError:
        print("Not a valid port. Please enter an integer.")
        setup_socket()
        return

    main_socket = socket.socket()

    # Socket refresh fix.
    main_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        main_socket.bind(("", tcp_port))
    except PermissionError:
        print("Port reserved by operating system. Choose another one.")
        setup_socket()
        return
    except OverflowError:
        print("Port is outside range. Port must be 0-65535")
        setup_socket()
        return

    main_socket.listen()

    print("Socket setup finished.")


def client_handler():
    while True:
        print("<client_handler>")
        time.sleep(1)


def handle_clients():
    print("Starting client handler thread.")
    client_handler_thread = threading.Thread(target=client_handler)
    client_handler_thread.daemon = True
    client_handler_thread.start()


def main_loop():
    print("<main_loop>")
    time.sleep(1)


def main():
    try:
        setup_socket()
        handle_clients()
        while True:
            main_loop()
    except (KeyboardInterrupt, SystemExit):
        print('\nReceived keyboard interrupt. Quitting.')


if __name__ == "__main__":
    main()
