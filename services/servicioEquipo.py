import socket
import mysql.connector
from mysql.connector import Error

def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='CyberCafeManager',
            user='root',
            password='root_password'
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind the socket to the port where the bus will listen
bus_address = ('localhost', 5000)
print('starting up on {} port {}'.format(*bus_address))
sock.bind(bus_address)

# Listen for incoming connections
sock.listen(1)

try:
    while True:
        print('waiting for a connection')
        client_socket, client_address = sock.accept()
        try:
            print('connection from', client_address)

            while True:
                try:
                    # Receive the message
                    amount_received = 0
                    amount_expected = client_socket.recv(5)
                    if not amount_expected:
                        break
                    amount_expected = int(amount_expected)
                    data = b''
                    while amount_received < amount_expected:
                        chunk = client_socket.recv(amount_expected - amount_received)
                        if not chunk:
                            break
                        data += chunk
                        amount_received += len(chunk)
                    
                    if not data:
                        break
                    
                    # Process the received message
                    print("Processing ...")
                    print('received {!r}'.format(data))
                    
                    servicio = data[:5].decode()
                    datos = data[5:].decode()
                    print(f"Service: {servicio}, Data: {datos}")
                    
                    if servicio == "CLOSE":
                        print("Closing connection with client")
                        break

                    dataArray = datos.split('-')
                    
                    db_connection = connect_db()
                    response = ""
                    
                    if db_connection is not None:
                        cursor = db_connection.cursor()
                        
                        if servicio == "CODAE":
                            query = "INSERT INTO Equipo (nombre, descripcion, tipo, tarifa) VALUES (%s, %s, %s, %s)"
                            cursor.execute(query, (dataArray[0], dataArray[1], dataArray[2], dataArray[3]))
                            db_connection.commit()
                            response = "CODAE-OK"
                        
                        elif servicio == "CODIU":
                            query = "SELECT * FROM Equipo WHERE id = %s"
                            cursor.execute(query, (dataArray[0],))
                            equipo = cursor.fetchone()
                            if equipo:
                                response = f"CODIU-{equipo[0]}-{equipo[1]}-{equipo[2]}-{equipo[3]}-{equipo[4]}"
                            else:
                                response = "CODIU-NOTFOUND"
                        
                        elif servicio == "CODIT":
                            query = "SELECT * FROM Equipo"
                            cursor.execute(query)
                            equipos = cursor.fetchall()
                            response = "CODIT-" + "-".join([f"{equipo[0]}-{equipo[1]}-{equipo[2]}-{equipo[3]}-{equipo[4]}" for equipo in equipos])
                        
                        elif servicio == "CODEE":
                            query = "DELETE FROM Equipo WHERE id = %s"
                            cursor.execute(query, (dataArray[0],))
                            db_connection.commit()
                            response = "CODEE-OK"
                        
                        elif servicio == "CODME":
                            query = "UPDATE Equipo SET nombre = %s, descripcion = %s, tipo = %s, tarifa = %s WHERE id = %s"
                            cursor.execute(query, (dataArray[1], dataArray[2], dataArray[3], dataArray[4], dataArray[0]))
                            db_connection.commit()
                            response = "CODME-OK"
                        
                        db_connection.close()
                    
                    # Send the response
                    if response == "":
                        response = f"{servicio}-ERROR"
                    response_length = len(response)
                    message = f"{response_length:05}{response}".encode()
                    print(f'sending message: {message}')
                    client_socket.sendall(message)
                except ValueError as e:
                    print(f"Error processing message: {e}")
                    break
        finally:
            client_socket.close()
finally:
    print('closing socket')
    sock.close()
