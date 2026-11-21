import sqlite3

with sqlite3.connect("usuarios.db") as conexion:
    for fila in conexion.execute(
        "SELECT id, nombre_usuario, hash_contrasena, fecha_registro FROM usuarios"
    ):
        print(fila)