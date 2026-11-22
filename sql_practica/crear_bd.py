import sqlite3

clientes = [
    (1, "Ana Torres", "Norte", "2024-01-15"),
    (2, "Luis Pérez", "Sur", "2024-02-03"),
    (3, "María Gómez", "Norte", "2024-03-21"),
    (4, "Carlos Ruiz", "Centro", "2024-04-10"),
    (5, "Sofía Díaz", "Sur", "2024-05-02"),
    (6, "Pedro Rojas", "Centro", "2024-06-18"),
]

productos = [
    (1, "Teclado", "Accesorios", 45.0),
    (2, "Mouse", "Accesorios", 25.0),
    (3, "Monitor", "Pantallas", 180.0),
    (4, "Portátil", "Computadores", 750.0),
    (5, "Auriculares", "Accesorios", 60.0),
    (6, "Tablet", "Computadores", 320.0),
]

pedidos = [
    (1, 1, "2024-07-01", "entregado"),
    (2, 1, "2024-07-15", "entregado"),
    (3, 2, "2024-07-20", "entregado"),
    (4, 3, "2024-08-02", "cancelado"),
    (5, 3, "2024-08-10", "entregado"),
    (6, 4, "2024-08-15", "pendiente"),
    (7, 2, "2024-09-01", "entregado"),
    (8, 5, "2024-09-05", "entregado"),
    (9, 1, "2024-09-12", "pendiente"),
    (10, 5, "2024-09-20", "entregado"),
]

detalle_pedido = [
    (1, 1, 4, 1), (2, 1, 2, 2), (3, 2, 5, 1), (4, 3, 3, 2),
    (5, 3, 1, 1), (6, 4, 6, 1), (7, 5, 1, 1), (8, 5, 2, 1),
    (9, 6, 4, 1), (10, 7, 6, 2), (11, 8, 5, 3), (12, 9, 3, 1),
    (13, 10, 2, 4), (14, 10, 1, 2),
]


def crear_bd():
    with sqlite3.connect("tienda.db") as conexion:
        conexion.execute("PRAGMA foreign_keys = ON")

        conexion.executescript("""
            DROP TABLE IF EXISTS detalle_pedido;
            DROP TABLE IF EXISTS pedidos;
            DROP TABLE IF EXISTS productos;
            DROP TABLE IF EXISTS clientes;

            CREATE TABLE clientes (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                zona TEXT NOT NULL,
                fecha_registro TEXT NOT NULL
            );

            CREATE TABLE productos (
                id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                categoria TEXT NOT NULL,
                precio REAL NOT NULL
            );

            CREATE TABLE pedidos (
                id INTEGER PRIMARY KEY,
                cliente_id INTEGER NOT NULL REFERENCES clientes(id),
                fecha TEXT NOT NULL,
                estado TEXT NOT NULL
            );

            CREATE TABLE detalle_pedido (
                id INTEGER PRIMARY KEY,
                pedido_id INTEGER NOT NULL REFERENCES pedidos(id),
                producto_id INTEGER NOT NULL REFERENCES productos(id),
                cantidad INTEGER NOT NULL
            );
        """)

        conexion.executemany("INSERT INTO clientes VALUES (?, ?, ?, ?)", clientes)
        conexion.executemany("INSERT INTO productos VALUES (?, ?, ?, ?)", productos)
        conexion.executemany("INSERT INTO pedidos VALUES (?, ?, ?, ?)", pedidos)
        conexion.executemany("INSERT INTO detalle_pedido VALUES (?, ?, ?, ?)", detalle_pedido)


if __name__ == "__main__":
    crear_bd()
    print("Base de datos tienda.db creada.")