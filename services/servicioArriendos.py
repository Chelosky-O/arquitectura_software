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
    if action == "CODAE":
        return arrendar_equipo(data[5:])
    else:
        return "ARRIENK, Acción inválida"

def arrendar_equipo(payload):
    try:
        rut_cliente, id_equipo, tiempo_arriendo = payload.split(',')
        tiempo_arriendo = int(tiempo_arriendo)
        
        # Calcular el monto usando el servicio de cobro
        monto = calcular_cobro(id_equipo, tiempo_arriendo)
        if monto is None:
            return "ARRIENK, Error en cálculo de cobro"
        
        # Registrar el arriendo en la base de datos
        query = f"INSERT INTO Arriendos (id_equipo, rut_usuario, fecha, tiempo_arriendo, monto, estado) VALUES ({id_equipo}, {rut_cliente}, NOW(), {tiempo_arriendo}, {monto}, TRUE)"
        cursor.execute(query)
        db_connection.commit()
        
        # Obtener la fecha de arriendo registrada
        cursor.execute("SELECT fecha FROM Arriendos ORDER BY id DESC LIMIT 1")
        fecha = cursor.fetchone()[0]
        
        return f"ARRIEOK,{fecha},{monto}"
    except Exception as e:
        return f"ARRIENK,Error: {str(e)}"

def calcular_cobro(id_equipo, tiempo_arriendo):
    try:
        message = f"{id_equipo},{tiempo_arriendo}"
        response = send_message("COBRO", "CODCP", message)
        
        response_parts = response.split(',')
        print(response)
        if response_parts[0] == "COBROOKK":
            return int(response_parts[1])
        else:
            return None
    except Exception as e:
        print(f"Error connecting to COBRO service: {str(e)}")
        return None

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

try:
    message = b'00010sinitARRIE'
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
