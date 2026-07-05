from flask import Flask
import sqlite3

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

DATABASE = "usuarios.db"


# Crear la base de datos
def crear_bd():

    conexion = sqlite3.connect(DATABASE)
    cursor = conexion.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    conexion.commit()
    conexion.close()


# Agregar usuario
def agregar_usuario(nombre, password):

    conexion = sqlite3.connect(DATABASE)
    cursor = conexion.cursor()

    hash_password = generate_password_hash(password)

    try:
        cursor.execute(
            "INSERT INTO usuarios(nombre,password) VALUES(?,?)",
            (nombre, hash_password)
        )
    except sqlite3.IntegrityError:
        pass

    conexion.commit()
    conexion.close()


# Validar usuario
def validar_usuario(nombre, password):

    conexion = sqlite3.connect(DATABASE)
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT password FROM usuarios WHERE nombre=?",
        (nombre,)
    )

    resultado = cursor.fetchone()

    conexion.close()

    if resultado:
        return check_password_hash(resultado[0], password)

    return False


@app.route("/")
def inicio():
    return """
    <h2>Servidor Flask funcionando correctamente</h2>
    <p>Puerto: 7500</p>
    """


if __name__ == "__main__":

    crear_bd()

    # Cambiar por los integrantes reales
    agregar_usuario("Guillermo Piccardo", "clave123")
    agregar_usuario("Ignacio Marin", "python2026")

    print("\nVALIDACIÓN DE USUARIOS\n")

    usuario = input("Usuario: ")
    password = input("Contraseña: ")

    if validar_usuario(usuario, password):
        print("Acceso permitido.")
    else:
        print("Usuario o contraseña incorrectos.")

    app.run(host="0.0.0.0", port=7500)
