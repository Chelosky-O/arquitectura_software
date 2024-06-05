import socket
import sys

def format_message(service_code, data):
    longitud_datos = len(service_code + data)
    message = f"{longitud_datos:05}{service_code}{data}".encode()
    return message

def send_message(sock, message, expect_response=True):
    print(f'Sending message: {message}')
    sock.sendall(message)
    
    if expect_response:
        # Look for the response
        print("Waiting for transaction")
        amount_received = 0
        amount_expected = int(sock.recv(5))
        data = b''
        while amount_received < amount_expected:
            chunk = sock.recv(amount_expected - amount_received)
            amount_received += len(chunk)
            data += chunk
        print("Received response: {!r}".format(data.decode()))

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the bus is listening
bus_address = ('localhost', 5000)
print('Connecting to {} port {}'.format(*bus_address))
sock.connect(bus_address)

try:
    while True:
        print("\nMenu:")
        print("1. Crear un equipo (CODAE)")
        print("2. Obtener información de un equipo (CODIU)")
        print("3. Obtener información de todos los equipos (CODIT)")
        print("4. Eliminar equipo (CODEE)")
        print("5. Modificar equipo (CODME)")
        print("6. Salir")
        choice = input("Elija una opción: ")

        if choice == "1":
            equipo = input("Nombre del equipo: ")
            descripcion = input("Descripción del equipo: ")
            tipo = input("Tipo de equipo: ")
            tarifa = input("Tarifa del equipo: ")
            datos = f"{equipo}-{descripcion}-{tipo}-{tarifa}"
            servicio = "CODAE"
            message = format_message(servicio, datos)
            send_message(sock, message)
        
        elif choice == "2":
            id_equipo = input("ID del equipo: ")
            datos = f"{id_equipo}"
            servicio = "CODIU"
            message = format_message(servicio, datos)
            send_message(sock, message)
        
        elif choice == "3":
            servicio = "CODIT"
            datos = ""
            message = format_message(servicio, datos)
            send_message(sock, message)
        
        elif choice == "4":
            id_equipo = input("ID del equipo: ")
            datos = f"{id_equipo}"
            servicio = "CODEE"
            message = format_message(servicio, datos)
            send_message(sock, message)
        
        elif choice == "5":
            id_equipo = input("ID del equipo: ")
            nombre = input("Nuevo nombre del equipo: ")
            descripcion = input("Nueva descripción del equipo: ")
            tipo = input("Nuevo tipo de equipo: ")
            tarifa = input("Nueva tarifa del equipo: ")
            datos = f"{id_equipo}-{nombre}-{descripcion}-{tipo}-{tarifa}"
            servicio = "CODME"
            message = format_message(servicio, datos)
            send_message(sock, message)
        
        elif choice == "6":
            print("Cerrando el cliente.")
            message = format_message("CLOSE", "")
            send_message(sock, message, expect_response=False)
            break
        
        else:
            print("Opción no válida. Por favor, intente de nuevo.")
finally:
    print('closing socket')
    sock.close()
