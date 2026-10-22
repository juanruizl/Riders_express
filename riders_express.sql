-- Esquema y datos de RiderExpress. Se puede ejecutar las veces que haga falta:
-- borra las tablas y las vuelve a crear.

DROP TABLE IF EXISTS LineaPedido;
DROP TABLE IF EXISTS Pedido;
DROP TABLE IF EXISTS Vehiculo;
DROP TABLE IF EXISTS Plato;
DROP TABLE IF EXISTS Restaurante;
DROP TABLE IF EXISTS Usuario;
DROP TABLE IF EXISTS Rider;
DROP TABLE IF EXISTS Tramo;
DROP TABLE IF EXISTS Reparto;
DROP TABLE IF EXISTS CodigoPostal;

CREATE TABLE Usuario (
    id_usuario INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    saldo REAL NOT NULL DEFAULT 0 CHECK (saldo >= 0),
    barrio TEXT NOT NULL
);
INSERT INTO Usuario VALUES (1, 'Lucía Fernández', 25.5, 'Salamanca');
INSERT INTO Usuario VALUES (2, 'Carlos Gómez', 10.0, 'Justicia');
INSERT INTO Usuario VALUES (3, 'María López', 42.75, 'Embajadores');
INSERT INTO Usuario VALUES (4, 'Javier Ruiz', 0.0, 'Guindalera');
INSERT INTO Usuario VALUES (5, 'Ana Martín', 15.2, 'Delicias');

CREATE TABLE Restaurante (
    id_restaurante INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    barrio TEXT NOT NULL
);
INSERT INTO Restaurante VALUES (1, 'Pizzería Napoli', 'Justicia');
INSERT INTO Restaurante VALUES (2, 'Sushi Madrid', 'Salamanca');
INSERT INTO Restaurante VALUES (3, 'Burger House', 'Embajadores');
INSERT INTO Restaurante VALUES (4, 'Taquería El Güero', 'Delicias');

CREATE TABLE Plato (
    id_plato INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    categoria TEXT NOT NULL,
    precio REAL NOT NULL CHECK (precio > 0),
    id_restaurante INTEGER NOT NULL,
    FOREIGN KEY (id_restaurante) REFERENCES Restaurante(id_restaurante)
);
INSERT INTO Plato VALUES (1, 'Pizza Margarita', 'Pizza', 9.5, 1);
INSERT INTO Plato VALUES (2, 'Pizza Cuatro Quesos', 'Pizza', 11.0, 1);
INSERT INTO Plato VALUES (3, 'Nigiri Salmón', 'Sushi', 6.5, 2);
INSERT INTO Plato VALUES (4, 'Maki Atún', 'Sushi', 7.8, 2);
INSERT INTO Plato VALUES (5, 'Hamburguesa Clásica', 'Hamburguesa', 8.9, 3);
INSERT INTO Plato VALUES (6, 'Hamburguesa BBQ', 'Hamburguesa', 10.5, 3);
INSERT INTO Plato VALUES (7, 'Tacos al Pastor', 'Mexicana', 8.0, 4);
INSERT INTO Plato VALUES (8, 'Burrito de Pollo', 'Mexicana', 7.5, 4);

CREATE TABLE Rider (
    id_rider INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    barrio TEXT
);
INSERT INTO Rider VALUES (1, 'Pablo Sánchez', 'Retiro');
INSERT INTO Rider VALUES (2, 'Elena Torres', 'Chamberí');
INSERT INTO Rider VALUES (3, 'Diego Navarro', 'Atocha');

CREATE TABLE Vehiculo (
    matricula TEXT PRIMARY KEY,
    tipo TEXT NOT NULL,
    marca TEXT NOT NULL,
    id_rider INTEGER NOT NULL,
    FOREIGN KEY (id_rider) REFERENCES Rider(id_rider)
);
INSERT INTO Vehiculo VALUES ('1234ABC', 'Moto', 'Honda', 1);
INSERT INTO Vehiculo VALUES ('5678DEF', 'Bicicleta', 'Orbea', 2);
INSERT INTO Vehiculo VALUES ('9012GHI', 'Moto', 'Yamaha', 3);

CREATE TABLE Pedido (
    id_pedido INTEGER PRIMARY KEY,
    fecha TEXT NOT NULL,
    id_usuario INTEGER NOT NULL,
    id_rider INTEGER,
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (id_rider) REFERENCES Rider(id_rider)
);
INSERT INTO Pedido VALUES (1, '2026-10-10 13:45', 1, 1);
INSERT INTO Pedido VALUES (2, '2026-10-10 20:30', 2, 2);
INSERT INTO Pedido VALUES (3, '2026-10-11 14:10', 3, 3);
INSERT INTO Pedido VALUES (4, '2026-10-12 21:05', 5, 1);
INSERT INTO Pedido VALUES (5, '2026-10-13 13:20', 4, 2);
-- pedido de varios restaurantes (Napoli, Burger House y El Güero), para el reto del viajante
INSERT INTO Pedido VALUES (6, '2026-10-14 14:00', 5, 3);

-- precio_unit: el pedido recuerda lo que costó cada plato cuando se pidió
CREATE TABLE LineaPedido (
    id_pedido INTEGER NOT NULL,
    id_plato INTEGER NOT NULL,
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unit REAL NOT NULL CHECK (precio_unit > 0),
    PRIMARY KEY (id_pedido, id_plato),
    FOREIGN KEY (id_pedido) REFERENCES Pedido(id_pedido),
    FOREIGN KEY (id_plato) REFERENCES Plato(id_plato)
);
INSERT INTO LineaPedido VALUES (1, 3, 2, 6.5);
INSERT INTO LineaPedido VALUES (1, 4, 1, 7.8);
INSERT INTO LineaPedido VALUES (2, 1, 1, 9.5);
INSERT INTO LineaPedido VALUES (2, 2, 1, 11.0);
INSERT INTO LineaPedido VALUES (3, 5, 2, 8.9);
INSERT INTO LineaPedido VALUES (3, 6, 1, 10.5);
INSERT INTO LineaPedido VALUES (4, 7, 3, 8.0);
INSERT INTO LineaPedido VALUES (5, 8, 2, 7.5);
INSERT INTO LineaPedido VALUES (6, 1, 1, 9.5);
INSERT INTO LineaPedido VALUES (6, 5, 1, 8.9);
INSERT INTO LineaPedido VALUES (6, 7, 1, 8.0);

-- Las aristas del mapa: minutos en moto entre barrios vecinos
CREATE TABLE Tramo (
    origen TEXT NOT NULL,
    destino TEXT NOT NULL,
    minutos INTEGER NOT NULL CHECK (minutos > 0),
    PRIMARY KEY (origen, destino)
);
INSERT INTO Tramo VALUES ('Salamanca', 'Guindalera', 6);
INSERT INTO Tramo VALUES ('Salamanca', 'Justicia', 9);
INSERT INTO Tramo VALUES ('Justicia', 'Embajadores', 8);
INSERT INTO Tramo VALUES ('Embajadores', 'Delicias', 7);
INSERT INTO Tramo VALUES ('Guindalera', 'Delicias', 18);
INSERT INTO Tramo VALUES ('Salamanca', 'Retiro', 5);
INSERT INTO Tramo VALUES ('Retiro', 'Atocha', 6);
INSERT INTO Tramo VALUES ('Atocha', 'Embajadores', 5);
INSERT INTO Tramo VALUES ('Atocha', 'Delicias', 9);
INSERT INTO Tramo VALUES ('Atocha', 'Legazpi', 8);
INSERT INTO Tramo VALUES ('Delicias', 'Legazpi', 5);
INSERT INTO Tramo VALUES ('Justicia', 'Chamberí', 6);
INSERT INTO Tramo VALUES ('Chamberí', 'Salamanca', 10);

-- Repartos del turno (para el algoritmo voraz)
CREATE TABLE Reparto (
    id_reparto INTEGER PRIMARY KEY,
    zona TEXT NOT NULL,
    inicio TEXT NOT NULL,
    fin TEXT NOT NULL,
    CHECK (inicio < fin)
);
INSERT INTO Reparto VALUES (1, 'Salamanca', '12:00', '13:00');
INSERT INTO Reparto VALUES (2, 'Retiro', '12:30', '13:30');
INSERT INTO Reparto VALUES (3, 'Chamberí', '13:00', '14:00');
INSERT INTO Reparto VALUES (4, 'Justicia', '13:30', '14:30');
INSERT INTO Reparto VALUES (5, 'Guindalera', '14:00', '15:00');
INSERT INTO Reparto VALUES (6, 'Embajadores', '14:15', '15:15');
INSERT INTO Reparto VALUES (7, 'Atocha', '15:00', '16:00');
INSERT INTO Reparto VALUES (8, 'Delicias', '15:30', '16:30');
INSERT INTO Reparto VALUES (9, 'Legazpi', '16:00', '17:00');
INSERT INTO Reparto VALUES (10, 'Salamanca', '16:30', '17:30');
