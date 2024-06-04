import socket

def rent_equipments():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bus_address = ('localhost', 5000)
    sock.connect(bus_address)

    try:
        # Initialize service
        message = b'00010sinitrntqp'
        sock.sendall(message)
        sinit = 1

        rentals = []

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

                if service_name == 'rntqp':
                    parts = service_data.split(',')
                    rentals.append({
                        'equipment_id': parts[0],
                        'client_rut': parts[1],
                        'rental_time': parts[2]
                    })
                    response = 'OKEquipment rented'
                else:
                    response = 'NKInvalid service'

                response_length = len(response)
                response_message = f'{response_length:05}{service_name}{response}'.encode()
                sock.sendall(response_message)

    finally:
        sock.close()

if __name__ == '__main__':
    rent_equipments()
