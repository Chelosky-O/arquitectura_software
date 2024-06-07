import socket

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

# Funciones para la gestión de equipos
def obtener_info_equipo(id_equipo):
    response = send_message("EQUIP", "CODIU", str(id_equipo))
    
    response_parts = response.split(',')
    
    # Extract the required information
    id = response_parts[1]
    nombre = response_parts[2]
    descripcion = response_parts[3]
    tipo = response_parts[4]
    tarifa = response_parts[5]
    
    # Print the formatted information
    print(f"ID: {id}")
    print(f"Nombre: {nombre}")
    print(f"Descripción: {descripcion}")
    print(f"Tipo: {tipo}")
    print(f"Tarifa: {tarifa}")
    #print(f"Respuesta: {response}")

def obtener_info_todos_equipos():
    response = send_message("EQUIP", "CODIT", "")
    response = response[10:]
   
    #Split the response string by '|'
    equipos = response.split('|')

    # Iterate through each user and print the formatted information
    for equipo in equipos:
        #print(equipo)
        response_parts = equipo.split(',')
        
        # Extract the required information
        id = response_parts[0]
        nombre = response_parts[1]
        descripcion = response_parts[2]
        tipo = response_parts[3]
        tarifa = response_parts[4]

        # Print the formatted information
        print(f"ID: {id}")
        print(f"Nombre: {nombre}")
        print(f"Descripción: {descripcion}")
        print(f"Tipo: {tipo}")
        print(f"Tarifa: {tarifa}")
        print("-----------------")

    #print(f"Respuesta: {response}")

def añadir_equipo(nombre, descripcion, tipo, tarifa):
    data = f"{nombre},{descripcion},{tipo},{tarifa}"
    response = send_message("EQUIP", "CODAE", data)
    print(f"Equipo: {nombre} ha sido añadido")

def eliminar_equipo(id_equipo):
    response = send_message("EQUIP", "CODEE", str(id_equipo))
    print(f"Equipo de ID: {id_equipo} ha sido eliminado")

def modificar_equipo(id_equipo, nombre, descripcion, tipo, tarifa):
    data = f"{id_equipo},{nombre},{descripcion},{tipo},{tarifa}"
    response = send_message("EQUIP", "CODME", data)
    print(f"Datos del equipo de ID: {id_equipo} han sido modificados")

# Funciones para la gestión de usuarios
def añadir_usuario(nombre, rut, email):
    data = f"{nombre},{rut},{email}"
    response = send_message("USUAR", "CODAU", data)
    print(f"Usuario de RUT: {rut} ha sido añadido")

def eliminar_usuario(rut):
    response = send_message("USUAR", "CODEU", str(rut))
    print(f"Usuario de RUT: {rut} ha sido eliminado")

def modificar_usuario():
    rut = input("Ingrese el RUT del usuario a modificar: ")
    nombre = input("Ingrese el nuevo nombre del usuario: ")
    email = input("Ingrese el nuevo email del usuario: ")
    data = f"{rut},{nombre},{email}"
    response = send_message("USUAR", "CODMU", data)
    print(f"Datos del usuario de RUT: {rut} han sido modificados")

def obtener_info_usuario(rut):
    response = send_message("USUAR", "CODIU", str(rut))
    
    response_parts = response.split(',')
    
    # Extract the required information
    nombre = response_parts[1]
    rut = response_parts[2]
    email = response_parts[3]
    
    # Print the formatted information
    print(f"Nombre: {nombre}")
    print(f"RUT: {rut}")
    print(f"Email: {email}")

def obtener_info_todos_usuarios():
    response = send_message("USUAR", "CODIT", "")
    #Split the response string by '|'
    response = response[10:]
    usuarios = response.split('|')
    
    # Iterate through each user and print the formatted information
    for usuario in usuarios:
        #print(usuario)
        response_parts = usuario.split(',')

        # Extract the required information
        nombre = response_parts[0]
        rut = response_parts[1]
        email = response_parts[2]
        
        # Print the formatted information
        print(f"Nombre: {nombre}")
        print(f"RUT: {rut}")
        print(f"Email: {email}")
        print("-----------------")


# # Funciones para la gestión de usuarios
# def crear_usuario(nombre, rut, email):
#     data = f"{nombre},{rut},{email}"
#     response = send_message("USUAR", "CODCU", data)
#     print(f"Respuesta: {response}")

# def borrar_usuario(rut):
#     response = send_message("USUAR", "CODBU", str(rut))
#     print(f"Respuesta: {response}")

# def modificar_usuario(nombre, rut, email):
#     data = f"{nombre},{rut},{email}"
#     response = send_message("USUAR", "CODMU", data)
#     print(f"Respuesta: {response}")

# def obtener_info_usuario(rut):
#     response = send_message("USUAR", "CODIU", str(rut))
    
#     response_parts = response.split(',')
    
#     # Extract the required information
#     nombre = response_parts[1]
#     rut = response_parts[2]
#     email = response_parts[3]
    
#     # Print the formatted information
#     print(f"Nombre: {nombre}")
#     print(f"RUT: {rut}")
#     print(f"Email: {email}")
#     #print(f"Respuesta: {response}")

# def obtener_info_todos_usuarios():
#     response = send_message("USUAR", "CODIT", "")
#     #Split the response string by '|'
#     response = response[10:]
#     usuarios = response.split('|')
    
#     # Iterate through each user and print the formatted information
#     for usuario in usuarios:
#         print(usuario)
#         response_parts = usuario.split(',')

#         # Extract the required information
#         nombre = response_parts[0]
#         rut = response_parts[1]
#         email = response_parts[2]
        
#         # Print the formatted information
#         print(f"Nombre: {nombre}")
#         print(f"RUT: {rut}")
#         print(f"Email: {email}")
#         print("-----------------")
    
#     #print(f"Respuesta: {response}")

# Funciones para la gestión de alimentos
def añadir_alimento(nombre, precio, stock):
    data = f"{nombre},{precio},{stock}"
    response = send_message("ALIME", "CODAA", data)
    print(f"Alimento: {nombre} ha sido añadido")

def eliminar_alimento(id_alimento):
    response = send_message("ALIME", "CODEA", str(id_alimento))
    print(f"Alimento de ID: {id_alimento} ha sido eliminado")

def modificar_alimento(id_alimento, nombre, precio, stock):
    data = f"{id_alimento},{nombre},{precio},{stock}"
    response = send_message("ALIME", "CODMA", data)
    print(f"Los datos del alimento de ID: {id_alimento} han sido modificados")

def obtener_info_alimento(id_alimento):
    response = send_message("ALIME", "CODIA", str(id_alimento))
    response_parts = response.split(',')
    
    # Extract the required information
    id = response_parts[1]
    nombre = response_parts[2]
    precio = response_parts[3]
    stock = response_parts[4]
    
    # Print the formatted information
    print(f"ID: {id}")
    print(f"Nombre: {nombre}")
    print(f"Precio: {precio}")
    print(f"Stock: {stock}")
    #print(f"Respuesta: {response}")

def obtener_info_todos_alimentos():
    response = send_message("ALIME", "CODIT", "")
    response = response[10:] 
    #Split the response string by '|'
    alimentos = response.split('|')
    
    # Iterate through each user and print the formatted information
    for alimento in alimentos:
        response_parts = alimento.split(',')
        
        id = response_parts[0]
        nombre = response_parts[1]
        precio = response_parts[2]
        stock = response_parts[3]
        
        # Print the formatted information
        print(f"ID: {id}")
        print(f"Nombre: {nombre}")
        print(f"Precio: {precio}")
        print(f"Stock: {stock}")
        print("-----------------")
    #print(f"Respuesta: {response}")

# Ejemplos de uso
try:
    while True:
        print("Menú de opciones:")
        print("1. Gestión de equipos")
        print("2. Gestión de usuarios")
        print("3. Gestión de alimentos")
        print("4. Salir")
        option = input("Seleccione una opción: ")
        
        if option == "1":
            print("Menú de gestión de equipos:")
            print("1. Añadir equipo")
            print("2. Eliminar equipo")
            print("3. Modificar equipo")
            print("4. Obtener información de un equipo")
            print("5. Obtener información de todos los equipos")
            print("6. Volver al menú principal")
            equip_option = input("Seleccione una opción: ")
            if equip_option == "1":
                nombre = input("Ingrese nombre del equipo: ")
                descripcion = input("Ingrese descripción del equipo: ")
                tipo = input("Ingrese tipo del equipo: ")
                tarifa = input("Ingrese tarifa del equipo: ")
                añadir_equipo(nombre, descripcion, tipo, tarifa)
            elif equip_option == "2":
                id_equipo = input("Ingrese ID del equipo: ")
                eliminar_equipo(id_equipo)
            elif equip_option == "3":
                id_equipo = input("Ingrese ID del equipo: ")
                nombre = input("Ingrese nuevo nombre del equipo: ")
                descripcion = input("Ingrese nueva descripción del equipo: ")
                tipo = input("Ingrese nuevo tipo del equipo: ")
                tarifa = input("Ingrese nueva tarifa del equipo: ")
                modificar_equipo(id_equipo, nombre, descripcion, tipo, tarifa)
            elif equip_option == "4":
                id_equipo = input("Ingrese ID del equipo: ")
                obtener_info_equipo(id_equipo)
            elif equip_option == "5":
                obtener_info_todos_equipos()
            elif equip_option == "6":
                continue
            else:
                print("Opción no válida")
        
        elif option == "2":
            print("Menú de gestión de usuarios:")
            print("1. Añadir usuario")
            print("2. Eliminar usuario")
            print("3. Modificar usuario")
            print("4. Obtener información de un usuario")
            print("5. Obtener información de todos los usuarios")
            print("6. Volver al menú principal")
            usuar_option = input("Seleccione una opción: ")
            if usuar_option == "1":
                nombre = input("Ingrese nombre del usuario: ")
                rut = input("Ingrese RUT del usuario: ")
                email = input("Ingrese email del usuario: ")
                añadir_usuario(nombre, rut, email)
            elif usuar_option == "2":
                rut = input("Ingrese RUT del usuario: ")
                eliminar_usuario(rut)
            elif usuar_option == "3":
                modificar_usuario()
            elif usuar_option == "4":
                rut = input("Ingrese RUT del usuario: ")
                obtener_info_usuario(rut)
            elif usuar_option == "5":
                obtener_info_todos_usuarios()
            elif usuar_option == "6":
                continue
            else:
                print("Opción no válida")

        # elif option == "2":
        #     print("Menú de gestión de usuarios:")
        #     print("1. Crear usuario")
        #     print("2. Borrar usuario")
        #     print("3. Modificar usuario")
        #     print("4. Obtener información de un usuario")
        #     print("5. Obtener información de todos los usuarios")
        #     print("6. Volver al menú principal")
        #     usuar_option = input("Seleccione una opción: ")
        #     if usuar_option == "1":
        #         nombre = input("Ingrese nombre del usuario: ")
        #         rut = input("Ingrese RUT del usuario: ")
        #         email = input("Ingrese email del usuario: ")
        #         crear_usuario(nombre, rut, email)
        #     elif usuar_option == "2":
        #         rut = input("Ingrese RUT del usuario: ")
        #         borrar_usuario(rut)
        #     elif usuar_option == "3":
        #         nombre = input("Ingrese nombre del usuario: ")
        #         rut = input("Ingrese RUT del usuario: ")
        #         email = input("Ingrese email del usuario: ")
        #         modificar_usuario(nombre, rut, email)
        #     elif usuar_option == "4":
        #         rut = input("Ingrese RUT del usuario: ")
        #         obtener_info_usuario(rut)
        #     elif usuar_option == "5":
        #         obtener_info_todos_usuarios()
        #     elif usuar_option == "6":
        #         continue
        #     else:
        #         print("Opción no válida")
        
        elif option == "3":
            print("Menú de gestión de alimentos:")
            print("1. Añadir alimento")
            print("2. Eliminar alimento")
            print("3. Modificar alimento")
            print("4. Obtener información de un alimento")
            print("5. Obtener información de todos los alimentos")
            print("6. Volver al menú principal")
            alime_option = input("Seleccione una opción: ")
            if alime_option == "1":
                nombre = input("Ingrese nombre del alimento: ")
                precio = input("Ingrese precio del alimento: ")
                stock = input("Ingrese stock del alimento: ")
                añadir_alimento(nombre, precio, stock)
            elif alime_option == "2":
                id_alimento = input("Ingrese ID del alimento: ")
                eliminar_alimento(id_alimento)
            elif alime_option == "3":
                id_alimento = input("Ingrese ID del alimento: ")
                nombre = input("Ingrese nombre del alimento: ")
                precio = input("Ingrese precio del alimento: ")
                stock = input("Ingrese stock del alimento: ")
                modificar_alimento(id_alimento, nombre, precio, stock)
            elif alime_option == "4":
                id_alimento = input("Ingrese ID del alimento: ")
                obtener_info_alimento(id_alimento)
            elif alime_option == "5":
                obtener_info_todos_alimentos()
            elif alime_option == "6":
                continue
            else:
                print("Opción no válida")
        
        elif option == "4":
            break
        
        else:
            print("Opción no válida")
finally:
    print('Cerrando el cliente')
    sock.close()
