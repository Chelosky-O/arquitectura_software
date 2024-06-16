import socket
import sys
import mysql.connector
from datetime import datetime

# Conectar a la base de datos
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root_password",
    database="CyberCafeManager"
)

cursor = db_connection.cursor()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the bus is listening
bus_address = ('localhost', 5000)
print('connecting to {} port {}'.format(*bus_address))
sock.connect(bus_address)

def handle_request(data):
    action = data[:5]
    payload = data[5:]
    if action == "CODAJ":
        return añadir_juego(payload)
    elif action == "CODEJ":
        return eliminar_juego(payload)
    elif action == "CODMJ":
        return modificar_juego(payload)
    elif action == "CODIU":
        return obtener_info_juego(payload)
    elif action == "CODIT":
        return obtener_info_todos_juegos()
    else:
        return "JUEGONK, Acción inválida"

def añadir_juego(payload):
    nombre, descripcion, id_equipo = payload.split(',')
    query = f"INSERT INTO Juegos (nombre, descripcion, id_equipo) VALUES ('{nombre}', '{descripcion}', {id_equipo})"
    cursor.execute(query)
    db_connection.commit()
    return f"JUEGOOK,{cursor.lastrowid}"

def eliminar_juego(id_juego):
    query = f"DELETE FROM Juegos WHERE id={id_juego}"
    cursor.execute(query)
    db_connection.commit()
    return "JUEGOOK, Juego eliminado"

def modificar_juego(payload):
    id_juego, nombre, descripcion, id_equipo = payload.split(',')
    query = f"UPDATE Juegos SET nombre='{nombre}', descripcion='{descripcion}', id_equipo={id_equipo} WHERE id={id_juego}"
    cursor.execute(query)
    db_connection.commit()
    return "JUEGOOK, Juego modificado"

def obtener_info_juego(id_juego):
    query = f"SELECT * FROM Juegos WHERE id={id_juego}"
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        id_juego, nombre, descripcion, id_equipo = result
        response = f"JUEGOOK,{id_juego},{nombre},{descripcion},{id_equipo}"
    else:
        response = "JUEGONK, Juego no encontrado"
    return response

def obtener_info_todos_juegos():
    query = "SELECT * FROM Juegos"
    cursor.execute(query)
    results = cursor.fetchall()
    response = "JUEGOOK," + "|".join([f"{row[0]},{row[1]},{row[2]},{row[3]}" for row in results])
    return response

try:
    message = b'00010sinitJUEGO'
    print('sending {!r}'.format(message))
    sock.sendall(message)
    sinit = 1
    while True:
        print("Waiting for transaction")
        amount_received = 0
        amount_expected = int(sock.recv(5))

        while amount_received < amount_expected:
            data = sock.recv(amount_expected - amount_received)
            amount_received += len(data)
        print("Processing ...")
        print('received {!r}'.format(data))
        if sinit == 1:
            sinit = 0
            print('Received sinit answer')
        else:
            print("Send answer")
            data = data.decode()[5:]  # Remove the first 5 characters (service name)
            response = handle_request(data)
            response_message = f"{len(response):05}{response}".encode()
            print('sending {!r}'.format(response_message))
            sock.sendall(response_message)
finally:
    print('closing socket')
    sock.close()
    cursor.close()
    db_connection.close()
