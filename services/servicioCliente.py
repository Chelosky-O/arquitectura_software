import socket
import mysql.connector
from mysql.connector import Error

def connect_db():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='CyberCafeManager',
            user='user',
            password='user_password'
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def handle_request(servicio, datos):
    response = ""
    db_connection = connect_db()
    if db_connection is None:
        return f"{servicio}NKFailed to connect to database"

    cursor = db_connection.cursor()

    if servicio == "CODAU":  # Añadir usuario
        dataArray = datos.split('-')
        query = "INSERT INTO Cliente (rut, nombre, email) VALUES (%s, %s, %s)"
        cursor.execute(query, (dataArray[0], dataArray[1], dataArray[2]))
        db_connection.commit()
        response = f"{servicio}OKUser added with RUT {dataArray[0]}"

    elif servicio == "CODEL":  # Eliminar usuario
        query = "DELETE FROM Cliente WHERE rut = %s"
        cursor.execute(query, (datos,))
        db_connection.commit()
        response = f"{servicio}OKUser with RUT {datos} deleted"

    elif servicio == "CODMU":  # Modificar usuario
        dataArray = datos.split('-')
        query = "UPDATE Cliente SET nombre = %s, email = %s WHERE rut = %s"
        cursor.execute(query, (dataArray[1], dataArray[2], dataArray[0]))
        db_connection.commit()
        response = f"{servicio}OKUser with RUT {dataArray[0]} updated"

    elif servicio == "CODGU":  # Obtener información del usuario
        query = "SELECT rut, nombre, email FROM Cliente WHERE rut = %s"
        cursor.execute(query, (datos,))
        result = cursor.fetchone()
        if result:
            response = f"{servicio}OK{result[0]}-{result[1]}-{result[2]}"
        else:
            response = f"{servicio}NKNo user found with RUT {datos}"

    db_connection.close()
    return response

def main():
    while True:
        # Create a TCP/IP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bus_address = ('localhost', 5000)
        print('connecting to {} port {}'.format(*bus_address))
        sock.connect(bus_address)

        try:
            while True:
                print('waiting for a connection')
                # Receive the message
                amount_received = 0
                amount_expected = int(sock.recv(5).decode())
                data = b''
                while amount_received < amount_expected:
                    chunk = sock.recv(amount_expected - amount_received)
                    if not chunk:
                        break
                    data += chunk
                    amount_received += len(chunk)

                if not data:
                    break

                print("Processing ...")
                print('received {!r}'.format(data))

                servicio = data[:5].decode()
                datos = data[5:].decode()
                print(f"Service: {servicio}, Data: {datos}")

                response = handle_request(servicio, datos)

                response_length = len(response)
                message = f"{response_length:05}{response}".encode()
                print('sending {!r}'.format(message))
                sock.sendall(message)
        finally:
            sock.close()

if __name__ == "__main__":
    main()
