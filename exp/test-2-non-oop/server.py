import queue
import select
import socket

DEFAULT_PORT = 13377

# Required global variables because this is not OOP yet.
tcp_port: int
server_socket: socket
input_sockets: list[socket]
output_sockets: list[socket]
message_queues: dict


def setup_server_socket():
    global tcp_port
    tcp_port = DEFAULT_PORT
    global server_socket

    try:
        tcp_port_string = input(f"Enter connection port [{DEFAULT_PORT}]: ")
        if tcp_port_string != "":
            tcp_port = int(tcp_port_string)
    except ValueError:
        print("Not a valid port. Please enter an integer.")
        setup_server_socket()
        return

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setblocking(False)

    # Socket refresh fix.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind(("", tcp_port))
    except PermissionError:
        print("Port reserved by operating system. Choose another one.")
        setup_server_socket()
        return
    except OverflowError:
        print("Port is outside range. Port must be 0-65535")
        setup_server_socket()
        return

    server_socket.listen(5)

    print("Socket setup finished.")


def assign_global_variables():
    global input_sockets
    global output_sockets
    global message_queues
    input_sockets = [server_socket]
    output_sockets = []
    message_queues = {}


def add_msg_to_all_queue(msg: str):
    for q in message_queues:
        if q is not server_socket:
            message_queues[q].put(msg)
            if q not in output_sockets:
                output_sockets.append(q)


def handle_sockets():
    print("Waiting for signal...")
    readable_sockets, writable_sockets, exceptional_sockets = select.select(
        input_sockets, output_sockets, input_sockets)

    for readable in readable_sockets:
        # If server socket is readable: add a new client.
        if readable is server_socket:
            connection, client_address = readable.accept()
            connection.setblocking(False)
            input_sockets.append(connection)
            message_queues[connection] = queue.Queue()
        else:
            msg = readable.recv(1024).decode()
            # If there is data from the socket: send it to all clients.
            if msg:
                if msg != '$SERVER_CLOSED':
                    add_msg_to_all_queue(msg)
            else:
                if readable in output_sockets:
                    output_sockets.remove(readable)
                input_sockets.remove(readable)
                readable.close()
                del message_queues[readable]

    for writable in writable_sockets:
        try:
            next_msg = message_queues[writable].get_nowait()
        except queue.Empty:
            output_sockets.remove(writable)
        else:
            writable.send(next_msg.encode())

    for exceptional in exceptional_sockets:
        input_sockets.remove(exceptional)
        if exceptional in output_sockets:
            output_sockets.remove(exceptional)
        exceptional.close()
        del message_queues[exceptional]

    print("Signal handled.")


def cleanup():
    try:
        for s in input_sockets:
            if s is not server_socket:
                s.send('$SERVER_CLOSED'.encode())
            s.close()
    except NameError:
        pass


def main():
    try:
        setup_server_socket()
        assign_global_variables()
        while True:
            handle_sockets()

    except (KeyboardInterrupt, SystemExit):
        print('\nReceived keyboard interrupt. Quitting.')
        cleanup()


if __name__ == "__main__":
    main()
