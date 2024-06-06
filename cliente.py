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

# Funciones para la gestión de equipos
def obtener_info_equipo(id_equipo):
    response = send_message("EQUIP", "CODIU", str(id_equipo))
    print(f"Respuesta: {response}")

def obtener_info_todos_equipos():
    response = send_message("EQUIP", "CODIT", "")
    print(f"Respuesta: {response}")

def añadir_equipo(nombre, descripcion, tipo, tarifa):
    data = f"{nombre},{descripcion},{tipo},{tarifa}"
    response = send_message("EQUIP", "CODAE", data)
    print(f"Respuesta: {response}")

def eliminar_equipo(id_equipo):
    response = send_message("EQUIP", "CODEE", str(id_equipo))
    print(f"Respuesta: {response}")

def modificar_equipo(id_equipo, nombre, descripcion, tipo, tarifa):
    data = f"{id_equipo},{nombre},{descripcion},{tipo},{tarifa}"
    response = send_message("EQUIP", "CODME", data)
    print(f"Respuesta: {response}")

# Funciones para la gestión de usuarios
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
        print("1. Gestión de equipos")
        print("2. Gestión de usuarios")
        print("3. Salir")
        option = input("Seleccione una opción: ")
        
        if option == "1":
            print("Menú de gestión de equipos:")
            print("1. Obtener información de un equipo")
            print("2. Obtener información de todos los equipos")
            print("3. Añadir equipo")
            print("4. Eliminar equipo")
            print("5. Modificar equipo")
            print("6. Volver al menú principal")
            equip_option = input("Seleccione una opción: ")
            if equip_option == "1":
                id_equipo = input("Ingrese ID del equipo: ")
                obtener_info_equipo(id_equipo)
            elif equip_option == "2":
                obtener_info_todos_equipos()
            elif equip_option == "3":
                nombre = input("Ingrese nombre del equipo: ")
                descripcion = input("Ingrese descripcion del equipo: ")
                tipo = input("Ingrese tipo del equipo: ")
                tarifa = input("Ingrese tarifa del equipo: ")
                añadir_equipo(nombre, descripcion, tipo, tarifa)
            elif equip_option == "4":
                id_equipo = input("Ingrese ID del equipo: ")
                eliminar_equipo(id_equipo)
            elif equip_option == "5":
                id_equipo = input("Ingrese ID del equipo: ")
                nombre = input("Ingrese nombre del equipo: ")
                descripcion = input("Ingrese descripcion del equipo: ")
                tipo = input("Ingrese tipo del equipo: ")
                tarifa = input("Ingrese tarifa del equipo: ")
                modificar_equipo(id_equipo, nombre, descripcion, tipo, tarifa)
            elif equip_option == "6":
                continue
            else:
                print("Opción no válida")
        
        elif option == "2":
            print("Menú de gestión de usuarios:")
            print("1. Crear usuario")
            print("2. Borrar usuario")
            print("3. Modificar usuario")
            print("4. Obtener información de un usuario")
            print("5. Obtener información de todos los usuarios")
            print("6. Volver al menú principal")
            usuar_option = input("Seleccione una opción: ")
            if usuar_option == "1":
                nombre = input("Ingrese nombre del usuario: ")
                rut = input("Ingrese RUT del usuario: ")
                email = input("Ingrese email del usuario: ")
                crear_usuario(nombre, rut, email)
            elif usuar_option == "2":
                rut = input("Ingrese RUT del usuario: ")
                borrar_usuario(rut)
            elif usuar_option == "3":
                nombre = input("Ingrese nombre del usuario: ")
                rut = input("Ingrese RUT del usuario: ")
                email = input("Ingrese email del usuario: ")
                modificar_usuario(nombre, rut, email)
            elif usuar_option == "4":
                rut = input("Ingrese RUT del usuario: ")
                obtener_info_usuario(rut)
            elif usuar_option == "5":
                obtener_info_todos_usuarios()
            elif usuar_option == "6":
                continue
            else:
                print("Opción no válida")
        
        elif option == "3":
            break
        
        else:
            print("Opción no válida")
finally:
    print('Cerrando el cliente')
    sock.close()
