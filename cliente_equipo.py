import socket
import sys
import json

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

# Ejemplos de uso
try:
    while True:
        print("Menú de opciones:")
        print("1. Obtener información de un equipo")
        print("2. Obtener información de todos los equipos")
        print("3. Añadir equipo")
        print("4. Eliminar equipo")
        print("5. Modificar equipo")
        print("6. Salir")
        option = input("Seleccione una opción: ")
        if option == "1":
            id_equipo = input("Ingrese ID del equipo: ")
            obtener_info_equipo(id_equipo)
        elif option == "2":
            obtener_info_todos_equipos()
        elif option == "3":
            nombre = input("Ingrese nombre del equipo: ")
            descripcion = input("Ingrese descripcion del equipo: ")
            tipo = input("Ingrese tipo del equipo: ")
            tarifa = input("Ingrese tarifa del equipo: ")
            añadir_equipo(nombre, descripcion, tipo, tarifa)
        elif option == "4":
            id_equipo = input("Ingrese ID del equipo: ")
            eliminar_equipo(id_equipo)
        elif option == "5":
            id_equipo = input("Ingrese ID del equipo: ")
            nombre = input("Ingrese nombre del equipo: ")
            descripcion = input("Ingrese descripcion del equipo: ")
            tipo = input("Ingrese tipo del equipo: ")
            tarifa = input("Ingrese tarifa del equipo: ")
            modificar_equipo(id_equipo, nombre, descripcion, tipo, tarifa)
        elif option == "6":
            break
        else:
            print("Opción no válida")
finally:
    print('Cerrando el cliente')
    sock.close()
