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
    else:
        return "EQUIPNK, Acción inválida"

def obtener_info_equipo(id_equipo):
    query = f"""
    SELECT e.id, e.nombre, e.descripcion, e.tipo, e.tarifa, a.fecha_fin 
    FROM Equipos e
    LEFT JOIN Arriendos a ON e.id = a.id_equipo
    WHERE e.id = {id_equipo}
    """
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        id_equipo, nombre, descripcion, tipo, tarifa, fecha_fin = result
        now = datetime.now().replace(microsecond=0)
        if fecha_fin is None or fecha_fin.replace(microsecond=0) < now:
            response = f"EQUIPOK,{id_equipo},{nombre},{descripcion},{tipo},{tarifa},No arrendado"
        else:
            response = f"EQUIPOK,{id_equipo},{nombre},{descripcion},{tipo},{tarifa},{fecha_fin}"
    else:
        response = "EQUIPNK, Equipo no encontrado"
    return response

def obtener_info_todos_equipos():
    # Recuperar todos los registros de equipos y arriendos
    query = """
    SELECT e.id, e.nombre, e.descripcion, e.tipo, e.tarifa, a.fecha_fin 
    FROM Equipos e
    LEFT JOIN Arriendos a ON e.id = a.id_equipo
    """
    cursor.execute(query)
    results = cursor.fetchall()

    # Separar dispositivos disponibles y arrendados en Python
    dispositivos_disponibles = []
    dispositivos_arrendados = []
    now = datetime.now().replace(microsecond=0)
    for row in results:
        id_equipo, nombre, descripcion, tipo, tarifa, fecha_fin = row
        if fecha_fin is None or fecha_fin.replace(microsecond=0) < now:
            dispositivos_disponibles.append(f"{id_equipo},{nombre},{descripcion},{tipo},{tarifa}")
        else:
            dispositivos_arrendados.append(f"{id_equipo},{nombre},{descripcion},{tipo},{tarifa}")
    
    response = "EQUIPOK,Disponibles:" + "|".join(dispositivos_disponibles) + ";Arrendados:" + "|".join(dispositivos_arrendados)
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
