CREATE DATABASE CyberCafeManager;

USE CyberCafeManager;

-- Tabla Equipos
CREATE TABLE Equipos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    tipo TEXT,
    tarifa INT
);

-- Tabla Usuarios
CREATE TABLE Usuarios (
    rut INT PRIMARY KEY,
    nombre TEXT NOT NULL,
    email TEXT
);

-- Tabla Arriendos
CREATE TABLE Arriendos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_equipo INT,
    rut_usuario INT,
    fecha DATE,
    tiempo_arriendo INT,
    monto INT,
    estado BOOLEAN,
    FOREIGN KEY (id_equipo) REFERENCES Equipos(id),
    FOREIGN KEY (rut_usuario) REFERENCES Usuarios(rut)
);

-- Tabla Alimentos
CREATE TABLE Alimentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre TEXT NOT NULL,
    precio INT,
    stock INT
);

-- Tabla VentasAlimentos
CREATE TABLE VentasAlimentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rut_usuario INT,
    id_comida INT,
    fecha DATE,
    total INT,
    FOREIGN KEY (rut_usuario) REFERENCES Usuarios(rut),
    FOREIGN KEY (id_comida) REFERENCES Alimentos(id)
);

-- Tabla Juegos
CREATE TABLE Juegos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    id_equipo INT,
    FOREIGN KEY (id_equipo) REFERENCES Equipos(id)
);
