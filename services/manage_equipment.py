import socket

def manage_equipments():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bus_address = ('localhost', 5000)
    sock.connect(bus_address)

    try:
        # Initialize service
        message = b'00010sinitmgeqp'
        sock.sendall(message)
        sinit = 1

        equipments = []

        while True:
            amount_received = 0
            amount_expected = int(sock.recv(5))

            while amount_received < amount_expected:
                data = sock.recv(amount_expected - amount_received)
                amount_received += len(data)

            if sinit == 1:
                sinit = 0
            else:
                request = data.decode()
                service_name = request[5:10]
                service_data = request[10:]

                if service_name == 'mgeqp':
                    parts = service_data.split(',')
                    if parts[0] == 'add':
                        equipments.append({
                            'name': parts[1],
                            'description': parts[2],
                            'type': parts[3],
                            'tariff': parts[4]
                        })
                        response = 'OKEquipment added'
                    else:
                        response = 'NKMisunderstood command'
                else:
                    response = 'NKInvalid service'

                response_length = len(response)
                response_message = f'{response_length:05}{service_name}{response}'.encode()
                sock.sendall(response_message)

    finally:
        sock.close()

if __name__ == '__main__':
    manage_equipments()
