import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the bus is listening
bus_address = ('localhost', 5000)
print('connecting to {} port {}'.format(*bus_address))
sock.connect(bus_address)

def send_message(service, action, data):
    message_data = f"{action}{data}"
    message = f"{len(message_data):05}{service}{message_data}".encode()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    bus_address = ('localhost', 5000)
    sock.connect(bus_address)
    try:
        sock.sendall(message)
        amount_expected = int(sock.recv(5))
        amount_received = 0
        response = b''
        while amount_received < amount_expected:
            chunk = sock.recv(amount_expected - amount_received)
            amount_received += len(chunk)
            response += chunk
    finally:
        sock.close()
    return response.decode()

def crear_usuario(nombre, rut, email):
    data = f"{nombre},{rut},{email}"
    response = send_message("USUAR", "CODCU", data)
    print(f"Respuesta: {response}")

def borrar_usuario(rut):
    response = send_message("USUAR", "CODBU", str(rut))
    print(f"Respuesta: {response}")

def modificar_usuario(nombre, rut, email):
    data = f"{nombre},{rut},{email}"
    response = send_message("USUAR", "CODMU", data)
    print(f"Respuesta: {response}")

def obtener_info_usuario(rut):
    response = send_message("USUAR", "CODIU", str(rut))
    print(f"Respuesta: {response}")

def obtener_info_todos_usuarios():
    response = send_message("USUAR", "CODIT", "")
    print(f"Respuesta: {response}")

# Ejemplos de uso
try:
    while True:
        print("Menú de opciones:")
        print("1. Crear usuario")
        print("2. Borrar usuario")
        print("3. Modificar usuario")
        print("4. Obtener información de un usuario")
        print("5. Obtener información de todos los usuarios")
        print("6. Salir")
        option = input("Seleccione una opción: ")
        if option == "1":
            nombre = input("Ingrese nombre del usuario: ")
            rut = input("Ingrese RUT del usuario: ")
            email = input("Ingrese email del usuario: ")
            crear_usuario(nombre, rut, email)
        elif option == "2":
            rut = input("Ingrese RUT del usuario: ")
            borrar_usuario(rut)
        elif option == "3":
            nombre = input("Ingrese nombre del usuario: ")
            rut = input("Ingrese RUT del usuario: ")
            email = input("Ingrese email del usuario: ")
            modificar_usuario(nombre, rut, email)
        elif option == "4":
            rut = input("Ingrese RUT del usuario: ")
            obtener_info_usuario(rut)
        elif option == "5":
            obtener_info_todos_usuarios()
        elif option == "6":
            break
        else:
            print("Opción no válida")
finally:
    print('Cerrando el cliente')
    sock.close()
