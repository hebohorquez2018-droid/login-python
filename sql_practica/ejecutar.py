import sqlite3
import sys


def mostrar(cursor):
    columnas = [d[0] for d in cursor.description]
    filas = cursor.fetchall()

    anchos = []
    for i, nombre in enumerate(columnas):
        ancho = len(nombre)
        for fila in filas:
            ancho = max(ancho, len(str(fila[i])))
        anchos.append(ancho)

    print(" | ".join(n.ljust(a) for n, a in zip(columnas, anchos)))
    print("-+-".join("-" * a for a in anchos))
    for fila in filas:
        print(" | ".join(str(v).ljust(a) for v, a in zip(fila, anchos)))
    print(f"({len(filas)} filas)\n")


def main():
    if len(sys.argv) != 2:
        print("Uso: python ejecutar.py consultas/archivo.sql")
        return

    with open(sys.argv[1], encoding="utf-8") as archivo:
        contenido = archivo.read()

    with sqlite3.connect("tienda.db") as conexion:
        for sentencia in contenido.split(";"):
            sentencia = sentencia.strip()
            if not sentencia:
                continue
            cursor = conexion.execute(sentencia)
            if cursor.description:
                mostrar(cursor)


if __name__ == "__main__":
    main()