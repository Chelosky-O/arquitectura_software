import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the bus is listening
bus_address = ('localhost', 5000)
print('connecting to {} port {}'.format(*bus_address))
sock.connect(bus_address)

try:
    while True:
        # Send message in the specified format
        if input('Send formatted message to service? y/n: ') != 'y':
            break

        # Show menu to the user
        print("Selecciona una opcion")
        print("1 - Agregar Usuario")
        print("2 - Eliminar Usuario")
        print("3 - Modificar Usuario")
        print("4 - Obtener Usuario")
        
        option = input("Elige la opcion (1/2/3/4): ")

        if option == "1":
            servicio = "CODAU"
            rut = input("Enter RUT: ")
            nombre = input("Enter name: ")
            email = input("Enter email: ")
            datos = f"{rut}-{nombre}-{email}"
        
        elif option == "2":
            servicio = "CODEL"
            rut = input("Enter RUT to delete: ")
            datos = rut
        
        elif option == "3":
            servicio = "CODMU"
            rut = input("Enter RUT to modify: ")
            nombre = input("Enter new name: ")
            email = input("Enter new email: ")
            datos = f"{rut}-{nombre}-{email}"
        
        elif option == "4":
            servicio = "CODGU"
            rut = input("Enter RUT to get: ")
            datos = rut
        
        else:
            print("Invalid option")
            continue
        
        longitud_datos = len(servicio + datos)
        message = f"{longitud_datos:05}{servicio}{datos}".encode()
        print('sending {!r}'.format(message))
        sock.sendall(message)
        
        # Look for the response
        print("Waiting for transaction")
        amount_received = 0
        amount_expected = int(sock.recv(5))
        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)
            print("Checking service answer ...")
            print('received {!r}'.format(data))
            
finally:
    print('closing socket')
    sock.close()
