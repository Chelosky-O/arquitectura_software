import subprocess
import os

# Obtiene la ruta del directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))

# Lista todos los archivos en el directorio actual
files = os.listdir(current_dir)

# Filtra solo los archivos .py
services = [file for file in files if file.endswith('.py') and file.startswith('servicio')]

# Ejecuta cada servicio en una nueva consola
for service in services:
    service_path = os.path.join(current_dir, service)
    if os.name == 'nt':  # Para Windows
        subprocess.Popen(['start', 'cmd', '/k', f'python {service_path}'], shell=True)
    else:  # Para Linux/macOS
        subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', f'python3 {service_path}; exec bash'])

print("Todos los servicios se están ejecutando en consolas separadas.")
