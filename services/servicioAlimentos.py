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
    if action == "CODAA":
        return agregar_alimento(payload)
    elif action == "CODQA":
        return quitar_alimento(payload)
    elif action == "CODMA":
        return modificar_alimento(payload)
    elif action == "CODIU":
        return obtener_info_alimento(payload)
    elif action == "CODIT":
        return obtener_info_todos_alimentos()
    else:
        return "ALIMENK,Invalid action"

def agregar_alimento(payload):
    nombre, precio, stock = payload.split(',')
    query = f"INSERT INTO Alimentos (nombre, precio, stock) VALUES ('{nombre}', {precio}, {stock})"
    try:
        cursor.execute(query)
        db_connection.commit()
        return f"ALIMEOK,{cursor.lastrowid}"
    except mysql.connector.Error as err:
        return f"ALIMENK,Error: {err}"

def quitar_alimento(id_alimento):
    query = f"DELETE FROM Alimentos WHERE id={id_alimento}"
    try:
        cursor.execute(query)
        db_connection.commit()
        return "ALIMEOK,Alimento eliminado"
    except mysql.connector.Error as err:
        return f"ALIMENK,Error: {err}"

def modificar_alimento(payload):
    id_alimento, nombre, precio, stock = payload.split(',')
    query = f"UPDATE Alimentos SET nombre='{nombre}', precio={precio}, stock={stock} WHERE id={id_alimento}"
    try:
        cursor.execute(query)
        db_connection.commit()
        return "ALIMEOK,Alimento modificado"
    except mysql.connector.Error as err:
        return f"ALIMENK,Error: {err}"

def obtener_info_alimento(id_alimento):
    query = f"SELECT * FROM Alimentos WHERE id={id_alimento}"
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        response = f"ALIMEOK,{result[0]},{result[1]},{result[2]},{result[3]}"
    else:
        response = "ALIMENK,Alimento no encontrado"
    return response

def obtener_info_todos_alimentos():
    query = "SELECT * FROM Alimentos"
    cursor.execute(query)
    results = cursor.fetchall()
    response = "ALIMEOK," + "|".join([f"{row[0]},{row[1]},{row[2]},{row[3]}" for row in results])
    return response

try:
    message = b'00010sinitALIME'
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