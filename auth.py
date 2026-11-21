import re
import sqlite3
from datetime import datetime, timedelta
MAX_INTENTOS = 3
MINUTOS_BLOQUEO = 5


from getpass import getpass

import bcrypt

from database import conectar, crear_tabla


def validar_contrasena(contrasena):
    if len(contrasena) < 8:
        return "La contraseña debe tener al menos 8 caracteres."
    if not re.search(r"[A-Z]", contrasena):
        return "Debe incluir al menos una mayúscula."
    if not re.search(r"[a-z]", contrasena):
        return "Debe incluir al menos una minúscula."
    if not re.search(r"\d", contrasena):
        return "Debe incluir al menos un número."
    return None


def registrar_usuario(nombre_usuario, contrasena):
    nombre_usuario = nombre_usuario.strip()

    if len(nombre_usuario) < 3:
        return False, "El nombre de usuario debe tener al menos 3 caracteres."

    error = validar_contrasena(contrasena)
    if error:
        return False, error

    hash_contrasena = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt())

    try:
        with conectar() as conexion:
            conexion.execute(
                "INSERT INTO usuarios (nombre_usuario, hash_contrasena) VALUES (?, ?)",
                (nombre_usuario, hash_contrasena.decode("utf-8")),
            )
    except sqlite3.IntegrityError:
        return False, "Ese nombre de usuario ya existe."

    return True, "Usuario registrado correctamente."


def iniciar_sesion(nombre_usuario, contrasena):
    nombre_usuario = nombre_usuario.strip()
    ahora = datetime.now()

    with conectar() as conexion:
        fila = conexion.execute(
            "SELECT hash_contrasena, intentos_fallidos, bloqueado_hasta "
            "FROM usuarios WHERE nombre_usuario = ?",
            (nombre_usuario,),
        ).fetchone()

        if fila is None:
            return False, "Usuario o contraseña incorrectos."

        hash_guardado, intentos, bloqueado_hasta = fila

        if bloqueado_hasta:
            fin_bloqueo = datetime.fromisoformat(bloqueado_hasta)
            if ahora < fin_bloqueo:
                minutos = int((fin_bloqueo - ahora).total_seconds() // 60) + 1
                return False, f"Cuenta bloqueada. Intenta de nuevo en {minutos} minuto(s)."

        if bcrypt.checkpw(contrasena.encode("utf-8"), hash_guardado.encode("utf-8")):
            conexion.execute(
                "UPDATE usuarios SET intentos_fallidos = 0, bloqueado_hasta = NULL "
                "WHERE nombre_usuario = ?",
                (nombre_usuario,),
            )
            return True, "Inicio de sesión exitoso."

        intentos += 1

        if intentos >= MAX_INTENTOS:
            nuevo_bloqueo = (ahora + timedelta(minutes=MINUTOS_BLOQUEO)).isoformat()
            conexion.execute(
                "UPDATE usuarios SET intentos_fallidos = 0, bloqueado_hasta = ? "
                "WHERE nombre_usuario = ?",
                (nuevo_bloqueo, nombre_usuario),
            )
            return False, f"Demasiados intentos. Cuenta bloqueada por {MINUTOS_BLOQUEO} minutos."

        conexion.execute(
            "UPDATE usuarios SET intentos_fallidos = ? WHERE nombre_usuario = ?",
            (intentos, nombre_usuario),
        )
        return False, "Usuario o contraseña incorrectos."

        

if __name__ == "__main__":
    crear_tabla()
    usuario = input("Nombre de usuario: ")
    clave = getpass("Contraseña: ")
    ok, mensaje = registrar_usuario(usuario, clave)
    print(mensaje)



    
# Qué hay de nuevo y por qué
# Hash, no cifrado reversible: bcrypt.hashpw convierte la contraseña en una cadena irreconocible que no se puede revertir. Para validar un login después, se compara la contraseña ingresada contra ese hash, nunca se “descifra”.
# Sal (gensalt): es un dato aleatorio que se mezcla con la contraseña. Gracias a eso, dos usuarios con la misma contraseña obtienen hashes distintos, y se frenan los ataques con tablas precalculadas. bcrypt la guarda dentro del propio hash, no necesitas una columna aparte.
# .encode("utf-8"): bcrypt trabaja con bytes, no con texto, así que convertimos el texto a bytes. Al guardar, hacemos el camino inverso con .decode("utf-8").
# Los ? en la consulta SQL: son parámetros. Nunca se arma una consulta pegando texto del usuario directamente en ella, porque eso permite un ataque llamado inyección SQL. Con ?, SQLite trata los valores solo como datos.
# try / except sqlite3.IntegrityError: como la columna nombre_usuario es UNIQUE, si intentas registrar un nombre repetido SQLite lanza ese error. Lo capturamos para mostrar un mensaje amable en lugar de que el programa se caiga.
# return False, "mensaje": la función devuelve dos valores (una tupla): si funcionó o no, y un mensaje. Así quien la llame decide qué mostrar.
# getpass: pide la contraseña sin mostrarla mientras la escribes. Ojo: en la terminal no verás nada al teclear, es normal.