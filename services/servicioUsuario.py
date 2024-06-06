import socket
import sys
import mysql.connector

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
    if action == "CODCU":
        return crear_usuario(payload)
    elif action == "CODBU":
        return borrar_usuario(payload)
    elif action == "CODMU":
        return modificar_usuario(payload)
    elif action == "CODIU":
        return obtener_info_usuario(payload)
    elif action == "CODIT":
        return obtener_info_todos_usuarios()
    else:
        return "USUARNK,Invalid action"

def crear_usuario(payload):
    nombre, rut, email = payload.split(',')
    query = f"INSERT INTO Cliente (rut, nombre, email) VALUES ('{rut}', '{nombre}', '{email}')"
    try:
        cursor.execute(query)
        db_connection.commit()
        return "USUAROK,Usuario creado"
    except mysql.connector.Error as err:
        return f"USUARNK,Error: {err}"

def borrar_usuario(rut):
    query = f"DELETE FROM Cliente WHERE rut='{rut}'"
    try:
        cursor.execute(query)
        db_connection.commit()
        return "USUAROK,Usuario eliminado"
    except mysql.connector.Error as err:
        return f"USUARNK,Error: {err}"

def modificar_usuario(payload):
    nombre, rut, email = payload.split(',')
    query = f"UPDATE Cliente SET nombre='{nombre}', email='{email}' WHERE rut='{rut}'"
    try:
        cursor.execute(query)
        db_connection.commit()
        return "USUAROK,Usuario modificado"
    except mysql.connector.Error as err:
        return f"USUARNK,Error: {err}"

def obtener_info_usuario(rut):
    query = f"SELECT * FROM Cliente WHERE rut='{rut}'"
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        response = f"USUAROK,{result[1]},{result[0]},{result[2]}"
    else:
        response = "USUARNK,Usuario no encontrado"
    return response

def obtener_info_todos_usuarios():
    query = "SELECT * FROM Cliente"
    cursor.execute(query)
    results = cursor.fetchall()
    response = "USUAROK," + "|".join([f"{row[1]},{row[0]},{row[2]}" for row in results])
    return response

try:
    message = b'00010sinitUSUAR'
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
