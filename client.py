import socket

def send_transaction(service, data):
    # Structure the message
    data_length = len(data)
    message = f'{data_length:05}{service:05}{data}'.encode()

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect the socket to the port where the bus is listening
    bus_address = ('localhost', 5000)
    sock.connect(bus_address)

    try:
        # Send the transaction
        sock.sendall(message)

        # Receive the response
        response_length = int(sock.recv(5).decode())
        response = sock.recv(response_length).decode()
        return response
    finally:
        sock.close()

def main():
    # Example usage of services
    print(send_transaction('mgeqp', 'add,PC1,High-end gaming PC,PC,10'))
    print(send_transaction('rntqp', '1,12345678,2'))
    print(send_transaction('chgeq', '1,2,20'))

if __name__ == '__main__':
    main()
