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
    if action == "CODIU":
        return obtener_info_equipo(payload)
    elif action == "CODIT":
        return obtener_info_todos_equipos()
    elif action == "CODAE":
        return añadir_equipo(payload)
    elif action == "CODEE":
        return eliminar_equipo(payload)
    elif action == "CODME":
        return modificar_equipo(payload)
    elif action == "DISPO":
        if payload == "disponibles":
            return obtener_dispositivos_disponibles()
        elif payload == "no_disponibles":
            return obtener_dispositivos_no_disponibles()
        else:
            return "EQUIPNK, Acción inválida"
    else:
        return "EQUIPNK, Acción inválida"

def obtener_info_equipo(id_equipo):
    query = f"SELECT * FROM Equipos WHERE id={id_equipo}"
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        response = f"EQUIPOK,{result[0]},{result[1]},{result[2]},{result[3]},{result[4]}"
    else:
        response = "EQUIPNK, Equipos no encontrados"
    return response

def obtener_info_todos_equipos():
    query = "SELECT * FROM Equipos"
    cursor.execute(query)
    results = cursor.fetchall()
    response = "EQUIPOK," + "|".join([f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]}" for row in results])
    return response

def obtener_dispositivos_disponibles():
    # Recuperar todos los registros de equipos y arriendos
    query = """
    SELECT e.id, e.nombre, a.fecha_fin FROM Equipos e
    LEFT JOIN Arriendos a ON e.id = a.id_equipo
    """
    cursor.execute(query)
    results = cursor.fetchall()

    # Filtrar dispositivos disponibles en Python
    dispositivos_disponibles = []
    for row in results:
        id_equipo, nombre_equipo, fecha_fin = row
        if fecha_fin is None or fecha_fin < datetime.now():
            dispositivos_disponibles.append(f"{id_equipo} - {nombre_equipo}")
    
    if dispositivos_disponibles:
        response = "EQUIPOK," + ",".join(dispositivos_disponibles)
    else:
        response = "EQUIPOK,No hay dispositivos disponibles"
    return response

def obtener_dispositivos_no_disponibles():
    # Recuperar todos los registros de equipos y arriendos
    query = """
    SELECT e.id, e.nombre, a.fecha_fin FROM Equipos e
    LEFT JOIN Arriendos a ON e.id = a.id_equipo
    """
    cursor.execute(query)
    results = cursor.fetchall()

    # Filtrar dispositivos no disponibles en Python
    dispositivos_no_disponibles = []
    for row in results:
        id_equipo, nombre_equipo, fecha_fin = row
        if fecha_fin is not None and fecha_fin > datetime.now():
            dispositivos_no_disponibles.append(f"{id_equipo} - {nombre_equipo}")
    
    if dispositivos_no_disponibles:
        response = "EQUIPOK," + ",".join(dispositivos_no_disponibles)
    else:
        response = "EQUIPOK,No hay dispositivos no disponibles"
    return response

def añadir_equipo(payload):
    nombre, descripcion, tipo, tarifa = payload.split(',')
    query = f"INSERT INTO Equipos (nombre, descripcion, tipo, tarifa) VALUES ('{nombre}', '{descripcion}', '{tipo}', {tarifa})"
    cursor.execute(query)
    db_connection.commit()
    return f"EQUIPOK,{cursor.lastrowid}"

def eliminar_equipo(id_equipo):
    query = f"DELETE FROM Equipos WHERE id={id_equipo}"
    cursor.execute(query)
    db_connection.commit()
    return "EQUIPOK, Equipo eliminado"

def modificar_equipo(payload):
    id_equipo, nombre, descripcion, tipo, tarifa = payload.split(',')
    query = f"UPDATE Equipos SET nombre='{nombre}', descripcion='{descripcion}', tipo='{tipo}', tarifa={tarifa} WHERE id={id_equipo}"
    cursor.execute(query)
    db_connection.commit()
    return "EQUIPOK, Equipo modificado"

try:
    message = b'00010sinitEQUIP'
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
