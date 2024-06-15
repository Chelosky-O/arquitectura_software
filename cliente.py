import socket
import json
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
    
    id = response_parts[1]
    nombre = response_parts[2]
    descripcion = response_parts[3]
    tipo = response_parts[4]
    tarifa = response_parts[5]
    arrendado = response_parts[6]

    if arrendado == "No arrendado":
        print(f"ID: {id}")
        print(f"Nombre: {nombre}")
        print(f"Descripción: {descripcion}")
        print(f"Tipo: {tipo}")
        print(f"Tarifa: {tarifa}")
    else:
        print(f"ID: {id}")
        print(f"Nombre: {nombre}")
        print(f"Descripción: {descripcion}")
        print(f"Tipo: {tipo}")
        print(f"Tarifa: {tarifa}")
        print(f"Arrendado: {arrendado}")

def obtener_info_todos_equipos():
    response = send_message("EQUIP", "CODIT", "")
    response = response[10:]
    
    # Separar respuesta en disponibles y arrendados
    partes = response.split(';')
    disponibles = partes[0].replace("Disponibles:", "").split('|')
    arrendados = partes[1].replace("Arrendados:", "").split('|')

    # Mostrar dispositivos disponibles
    print("Dispositivos Disponibles:")
    for equipo in disponibles:
        if equipo:
            response_parts = equipo.split(',')
            id = response_parts[0]
            nombre = response_parts[1]
            descripcion = response_parts[2]
            tipo = response_parts[3]
            tarifa = response_parts[4]
            print(f"ID: {id}")
            print(f"Nombre: {nombre}")
            print(f"Descripción: {descripcion}")
            print(f"Tipo: {tipo}")
            print(f"Tarifa: {tarifa}")
            print("-----------------")

    # Mostrar dispositivos arrendados
    print("Dispositivos Arrendados:")
    for equipo in arrendados:
        if equipo:
            response_parts = equipo.split(',')
            id = response_parts[0]
            nombre = response_parts[1]
            descripcion = response_parts[2]
            tipo = response_parts[3]
            tarifa = response_parts[4]
            print(f"ID: {id}")
            print(f"Nombre: {nombre}")
            print(f"Descripción: {descripcion}")
            print(f"Tipo: {tipo}")
            print(f"Tarifa: {tarifa}")
            print("-----------------")

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
    
def obtener_dispositivos_disponibles():
    response = send_message("EQUIP", "DISPO", "disponibles")
    dispositivos = response.split(',')
    for dispositivo in dispositivos:
        print(dispositivo)

def obtener_dispositivos_no_disponibles():
    response = send_message("EQUIP", "DISPO", "no_disponibles")
    dispositivos = response.split(',')
    for dispositivo in dispositivos:
        print(dispositivo)    

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

def arrendar_equipo(rut_cliente, id_equipo, tiempo_arriendo):
    data = f"{rut_cliente},{id_equipo},{tiempo_arriendo}"
    response = send_message("ARRIE", "CODAE", data)
    
    response_parts = response.split(',')
    print(response_parts[0])
    if response_parts[0] == "ARRIEOKOK":
        fecha = response_parts[1]
        monto = response_parts[2]
        fecha_fin = response_parts[3]
        print(f"Arriendo exitoso: Fecha inicio: {fecha},Fecha final: {fecha_fin}, Monto : {monto}")
    else:
        print("Error: ", response_parts[1])



# Funciones para la venta de alimentos
def vender_alimento(rut_usuario, nombre_alimento, cantidad):
    data = f"{rut_usuario},{nombre_alimento},{cantidad}"
    response = send_message("VENAL", "CODAC", data)
    
    response_parts = response.split(',')
    print(response_parts[0])
    if response_parts[0] == "VENALOKOK":
        total = response_parts[1]
        print(f"Total: {total}")
    else:
        print("Error: ", response_parts[1])

    
# Funciones para el registro de ganancias
def obtener_ganancias_arriendo(fecha_inicio, fecha_fin):
    data = f"{fecha_inicio},{fecha_fin}"
    response = send_message("REGAN", "CODAE", data)
    #print(response)
    response_parts = response.split(',',1)
    if response_parts[0] == "REGANOKOK":
        ganancias = response_parts[1].split('|')
        for ganancia in ganancias:
            #print(f"Procesando: {ganancia}")  # Agrega esta línea para depuración
            if ',' in ganancia:
                fecha, monto = ganancia.split(',')
                print(f"Fecha: {fecha}, Monto: {monto}")
            else:
                print(f"Formato incorrecto: {ganancia}")
    else:
        print("Error: ", response_parts[1])

def obtener_ganancias_ventas(fecha_inicio, fecha_fin):
    data = f"{fecha_inicio},{fecha_fin}"
    response = send_message("REGAN", "CODVA", data)
    
    response_parts = response.split(',',1)
    print(response_parts)
    if response_parts[0] == "REGANOKOK":
        ganancias = response_parts[1].split('|')
        for ganancia in ganancias:
            #print(f"Procesando: {ganancia}")  # Agrega esta línea para depuración
            if ',' in ganancia:
                fecha, monto = ganancia.split(',')
                print(f"Fecha: {fecha}, Monto: {monto}")
            else:
                print(f"Formato incorrecto: {ganancia}")
    else:
        print("Error: ", response_parts[1])

    
    
# Funciones para la generación de informes
def generar_informe_ganancia_equipos():
    response = send_message("INFOR", "CODGG", "")
    response_parts = response.split(',',1)
    print(response_parts)
    if response_parts[0] == "INFOROKOK":
        print("Montos por tipo de equipo:")
        montos_por_tipo = response_parts[1].split('|')
        
        for i, tipo_monto in enumerate(montos_por_tipo):
            subpartes = tipo_monto.split(',')
            if i < len(montos_por_tipo) - 1:  # Todos excepto el último elemento
                print(f"Equipo {i + 1}: {subpartes[0]},{subpartes[1]}")
            else:  # Último elemento
                print(f"Equipo {i + 1}: {subpartes[0]},{subpartes[1]}")
                print(f"Monto total: {subpartes[-1]}")
    else:
        print("Error al generar el informe: ", response_parts[1])

def generar_informe_uso_equipos():
    response = send_message("INFOR", "CODGU", "")
    response_parts = response.split(',',1)
    if response_parts[0] == "INFOROKOK":
        print("Uso de equipos:")
        uso_equipos = response_parts[1]  # All except the first element
        #print(uso_equipos)
        uso_equipos = uso_equipos.split('|')
        #print(uso_equipos)
        for equipo in uso_equipos:
            id_equipo, nombre, tiempo = equipo.split(',')
            print(f"ID Equipo: {id_equipo}, Nombre: {nombre}, Tiempo: {tiempo}")
    else:
        print("Error al generar el informe: ", response_parts[1])

def generar_informe_ventas():
    response = send_message("INFOR", "CODGV", "")
    response_parts = response.split(',',1)
    if response_parts[0] == "INFOROKOK":
        print("Ventas de alimentos:")
        ventas_alimentos = response_parts[1].split('|')  # All except the first and last elements

        for i, alimento in enumerate(ventas_alimentos):
            subpartes = alimento.split(',')
            print(subpartes)
            if i < len(ventas_alimentos) - 1:  # Todos excepto el último elemento
                print(f"Alimento {i + 1}: ID {subpartes[0]},Nombre {subpartes[1]},Monto {subpartes[2]} ")
            else:  # Último elemento
                print(f"Alimento {i + 1}: ID {subpartes[0]},Nombre {subpartes[1]},Monto {subpartes[2]} ")
                print(f"Monto total: {subpartes[-1]}")
        
    else:
        print("Error al generar el informe: ", response_parts[1])

# Funciones para la gestión de juegos
def agregar_juego(nombre, descripcion, id_equipo):
    data = f"{nombre},{descripcion},{id_equipo}"
    response = send_message("JUEGO", "CODAJ", data)
    print(f"Juego: {nombre} ha sido añadido con ID: {response.split(',')[1]}")

def quitar_juego(id_juego):
    response = send_message("JUEGO", "CODQJ", str(id_juego))
    print(f"Juego de ID: {id_juego} ha sido eliminado")

def modificar_juego(id_juego, nombre, descripcion, id_equipo):
    data = f"{id_juego},{nombre},{descripcion},{id_equipo}"
    response = send_message("JUEGO", "CODMJ", data)
    print(f"Datos del juego de ID: {id_juego} han sido modificados")

def obtener_info_juego(id_juego):
    response = send_message("JUEGO", "CODIU", str(id_juego))
    response_parts = response.split(',')
    if response_parts[0] == "JUEGOOK":
        id_juego = response_parts[1]
        nombre = response_parts[2]
        descripcion = response_parts[3]
        id_equipo = response_parts[4]
        print(f"ID: {id_juego}")
        print(f"Nombre: {nombre}")
        print(f"Descripción: {descripcion}")
        print(f"ID Equipo: {id_equipo}")
    else:
        print("Juego no encontrado")

def obtener_info_todos_juegos():
    response = send_message("JUEGO", "CODIT", "")
    response = response[10:]  # Assuming we need to strip the first 10 characters
    juegos = response.split('|')
    for juego in juegos:
        response_parts = juego.split(',')
        id_juego = response_parts[0]
        nombre = response_parts[1]
        descripcion = response_parts[2]
        id_equipo = response_parts[3]
        print(f"ID: {id_juego}")
        print(f"Nombre: {nombre}")
        print(f"Descripción: {descripcion}")
        print(f"ID Equipo: {id_equipo}")
        print("-----------------")

# Ejemplos de uso
try:
    while True:
        print("Menú de opciones:")
        print("1. Gestión de equipos")
        print("2. Gestión de usuarios")
        print("3. Gestión de alimentos")
        print("4. Gestión de juegos")
        print("5. Arriendo de equipos")
        print("6. Venta de alimentos")
        print("7. Registro de ganancias")
        print("8. Informes")
        print("9. Salir")
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
            print("Menú de gestión de juegos:")
            print("1. Agregar juego")
            print("2. Quitar juego")
            print("3. Modificar juego")
            print("4. Obtener información de un juego")
            print("5. Obtener información de todos los juegos")
            print("6. Volver al menú principal")
            juego_option = input("Seleccione una opción: ")
            if juego_option == "1":
                nombre = input("Ingrese nombre del juego: ")
                descripcion = input("Ingrese descripción del juego: ")
                id_equipo = input("Ingrese ID del equipo asociado al juego: ")
                agregar_juego(nombre, descripcion, id_equipo)
            elif juego_option == "2":
                id_juego = input("Ingrese ID del juego: ")
                quitar_juego(id_juego)
            elif juego_option == "3":
                id_juego = input("Ingrese ID del juego: ")
                nombre = input("Ingrese nuevo nombre del juego: ")
                descripcion = input("Ingrese nueva descripción del juego: ")
                id_equipo = input("Ingrese nuevo ID del equipo asociado al juego: ")
                modificar_juego(id_juego, nombre, descripcion, id_equipo)
            elif juego_option == "4":
                id_juego = input("Ingrese ID del juego: ")
                obtener_info_juego(id_juego)
            elif juego_option == "5":
                obtener_info_todos_juegos()
            elif juego_option == "6":
                continue
            else:
                print("Opción no válida")
        elif option == "5":
            print("Menú de arriendo de equipos:")
            print("1. Arrendar equipo")
            print("2. Volver al menú principal")
            arrie_option = input("Seleccione una opción: ")
            if arrie_option == "1":
                rut_cliente = input("Ingrese RUT del cliente: ")
                id_equipo = input("Ingrese ID del equipo: ")
                tiempo_arriendo = input("Ingrese tiempo de arriendo en horas: ")
                arrendar_equipo(rut_cliente, id_equipo, tiempo_arriendo)
            elif arrie_option == "2":
                continue
            else:
                print("Opción no válida")
                
        elif option == "6":
            print("Menú de venta de alimentos:")
            print("1. Vender alimento")
            print("2. Volver al menú principal")
            venal_option = input("Seleccione una opción: ")
            if venal_option == "1":
                rut_usuario = input("Ingrese RUT del usuario: ")
                nombre_alimento = input("Ingrese nombre del alimento: ")
                cantidad = input("Ingrese cantidad del alimento: ")
                vender_alimento(rut_usuario, nombre_alimento, cantidad)
            elif venal_option == "2":
                continue
            else:
                print("Opción no válida")

                
        elif option == "7":
            print("Menú de registro de ganancias:")
            print("1. Obtener registro de ganancias por arriendo de equipos")
            print("2. Obtener registro de ganancias por venta de alimentos")
            print("3. Volver al menú principal")
            regan_option = input("Seleccione una opción: ")
            if regan_option == "1":
                fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
                fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ")
                obtener_ganancias_arriendo(fecha_inicio, fecha_fin)
            elif regan_option == "2":
                fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
                fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ")
                obtener_ganancias_ventas(fecha_inicio, fecha_fin)
            elif regan_option == "3":
                continue
            else:
                print("Opción no válida")
                
        elif option == "8":
            print("Menú de informes:")
            print("1. Generar informe de ganancia por tipos de equipos")
            print("2. Generar informe de uso de equipos")
            print("3. Generar informe de ventas de alimentos")
            print("4. Volver al menú principal")
            infor_option = input("Seleccione una opción: ")
            if infor_option == "1":
                generar_informe_ganancia_equipos()
            elif infor_option == "2":
                generar_informe_uso_equipos()
            elif infor_option == "3":
                generar_informe_ventas()
            elif infor_option == "4":
                continue
            else:
                print("Opción no válida")   
                     
        elif option == "9":
            break
        
        else:
            print("Opción no válida")
finally:
    print('Cerrando el cliente')
    sock.close()
