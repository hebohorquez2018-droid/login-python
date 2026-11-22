import os
import psycopg
from dotenv import load_dotenv

load_dotenv()


def conectar():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )


def crear_tabla():
    with conectar() as conexion:
        conexion.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                nombre_usuario TEXT NOT NULL UNIQUE,
                hash_contrasena TEXT NOT NULL,
                fecha_registro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                intentos_fallidos INTEGER NOT NULL DEFAULT 0,
                bloqueado_hasta TIMESTAMP
            )
        """)


if __name__ == "__main__":
    crear_tabla()
    print("Base de datos lista.")