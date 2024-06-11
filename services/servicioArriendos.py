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
    if action == "CODAE":
        return arrendar_equipo(payload)
    else:
        return "ARRIENK, Acción inválida"

def arrendar_equipo(payload):
    rut_cliente, id_equipo, tiempo_arriendo = payload.split(',')
    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Usar servicio COBRO para calcular el monto total
    monto_total = calcular_monto(id_equipo, tiempo_arriendo)
    if monto_total is None:
        return "ARRIENK, Error en cálculo de cobro"

    # Insertar arriendo
    query = f"INSERT INTO Arriendos (id_equipo, rut_usuario, fecha, tiempo_arriendo, monto, estado) VALUES ({id_equipo}, {rut_cliente}, '{fecha}', {tiempo_arriendo}, {monto_total}, 1)"
    try:
        cursor.execute(query)
        db_connection.commit()
        id_arriendo = cursor.lastrowid
        return f"ARRIEOK,{id_arriendo},{fecha},{monto_total}"
    except mysql.connector.Error as err:
        return f"ARRIENK, Error: {err}"

def calcular_monto(id_equipo, tiempo_arriendo):
    # Conectar al servicio COBRO para calcular el monto total
    try:
        cobro_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cobro_bus_address = ('localhost', 5001)  # Puerto donde el servicio COBRO está escuchando
        cobro_sock.connect(cobro_bus_address)
        data = f"{id_equipo},{tiempo_arriendo}"
        message = f"{len(data):05}CODCP{data}".encode()
        cobro_sock.sendall(message)
        amount_expected = int(cobro_sock.recv(5))
        amount_received = 0
        response = b''
        while amount_received < amount_expected:
            chunk = cobro_sock.recv(amount_expected - amount_received)
            amount_received += len(chunk)
            response += chunk
        cobro_sock.close()
        response = response.decode()
        if response.startswith("COBROOK"):
            return int(response.split(',')[1])
        else:
            return None
    except Exception as e:
        print(f"Error connecting to COBRO service: {e}")
        return None

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
