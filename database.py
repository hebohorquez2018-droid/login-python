import sqlite3

NOMBRE_BD = "usuarios.db"


def conectar():
    return sqlite3.connect(NOMBRE_BD)


def crear_tabla():
    with conectar() as conexion:
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_usuario TEXT NOT NULL UNIQUE,
                hash_contrasena TEXT NOT NULL,
                fecha_registro TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                intentos_fallidos INTEGER NOT NULL DEFAULT 0,
                bloqueado_hasta TEXT
            )
        """)


if __name__ == "__main__":
    crear_tabla()
    print("Base de datos lista.")



#  import sqlite3 trae el módulo de SQLite que ya viene con Python.
# def conectar() es una función: un bloque de código con nombre que puedes reutilizar. Abre (o crea) el archivo usuarios.db.
# CREATE TABLE IF NOT EXISTS crea la tabla solo si todavía no existe, así puedes ejecutar el programa muchas veces sin errores.
# PRIMARY KEY AUTOINCREMENT hace que cada usuario tenga un número de identificación único que se asigna solo.
# UNIQUE impide que dos usuarios tengan el mismo nombre.
# hash_contrasena guardará la contraseña cifrada, nunca la contraseña real.
# if __name__ == "__main__": significa “ejecuta esto solo si corro este archivo directamente”. 
# Así más adelante podremos importar estas funciones desde otros archivos sin que se ejecute esa parte.