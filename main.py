from getpass import getpass

from auth import iniciar_sesion, registrar_usuario
from database import crear_tabla


def menu():
    crear_tabla()
    while True:
        print("\n--- Sistema de usuarios ---")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            usuario = input("Nombre de usuario: ")
            clave = getpass("Contraseña: ")
            ok, mensaje = registrar_usuario(usuario, clave)
            print(mensaje)
        elif opcion == "2":
            usuario = input("Nombre de usuario: ")
            clave = getpass("Contraseña: ")
            ok, mensaje = iniciar_sesion(usuario, clave)
            print(mensaje)
        elif opcion == "3":
            print("Hasta pronto.")
            break
        else:
            print("Opción no válida.")


if __name__ == "__main__":
    menu()