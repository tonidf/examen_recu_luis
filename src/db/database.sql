DROP DATABASE IF EXISTS tienda_examen;
CREATE DATABASE tienda_examen;
USE tienda_examen;

CREATE TABLE users(
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(250) NOT NULL
);

CREATE TABLE productos(
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    foto VARCHAR(250),
    cantidad VARCHAR(50),
    precio VARCHAR(50),
    descripcion VARCHAR(250)
)