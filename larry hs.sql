
SHOW ENGINES;


SHOW VARIABLES;


SET default_storage_engine='InnoDB';


DROP DATABASE AgendaContactos;


CREATE DATABASE IF NOT EXISTS AgendaContactos;
USE AgendaContactos;


SHOW DATABASES;

CREATE TABLE IF NOT EXISTS Usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    edad INT NOT NULL,
    genero ENUM('Masculino', 'Femenino', 'Otro') NOT NULL,
    intereses TEXT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
); 

SHOW TABLES;


CREATE TABLE IF NOT EXISTS Correos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    correo VARCHAR(255) NOT NULL UNIQUE,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id) ON DELETE CASCADE
);

SHOW TABLES;


CREATE TABLE IF NOT EXISTS Telefonos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    numero VARCHAR(20) NOT NULL UNIQUE,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(id) ON DELETE CASCADE
);

SHOW TABLES;

INSERT INTO Usuarios (nombre, edad, genero, intereses)
VALUES 
    ('Juan Pérez', 25, 'Masculino', 'Deportes, Música, Viajar'),
    ('María Gómez', 23, 'Femenino', 'Cine, Lectura, Cocina');

SELECT *FROM usuarios;

INSERT INTO Correos (usuario_id, correo)
VALUES 
    (1, 'juan.perez@example.com'),
    (2, 'maria.gomez@example.com');
SELECT *FROM Correos; 

SHOW TABLES;


INSERT INTO Telefonos (usuario_id, numero)
VALUES 
    (1, '555-1234'),
    (2, '555-5678');
SELECT *FROM telefonos;

SHOW TABLES;
