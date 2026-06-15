import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Nombre del archivo de la base de datos SQLite
DATABASE = "boam.db"


def conectar_db():
    """
    Crea y devuelve una conexion a la base de datos SQLite.
    row_factory permite acceder a los campos por nombre.
    """
    conexion = sqlite3.connect(DATABASE)
    conexion.row_factory = sqlite3.Row
    return conexion


def crear_base_datos():
    """
    Crea automaticamente la tabla reservas si no existe.
    """
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_cliente TEXT NOT NULL,
            telefono TEXT NOT NULL,
            servicio TEXT NOT NULL,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL
        )
    """)

    conexion.commit()
    conexion.close()


@app.route("/")
def index():
    """
    Ruta principal.
    Muestra todas las reservas registradas.
    """
    conexion = conectar_db()
    reservas = conexion.execute(
        "SELECT * FROM reservas ORDER BY fecha, hora"
    ).fetchall()
    conexion.close()

    return render_template("index.html", reservas=reservas)


@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    """
    Ruta para registrar una nueva reserva.
    Recibe los datos del formulario y los guarda en SQLite.
    """
    if request.method == "POST":
        nombre_cliente = request.form["nombre_cliente"]
        telefono = request.form["telefono"]
        servicio = request.form["servicio"]
        fecha = request.form["fecha"]
        hora = request.form["hora"]

        conexion = conectar_db()
        conexion.execute("""
            INSERT INTO reservas (
                nombre_cliente,
                telefono,
                servicio,
                fecha,
                hora
            ) VALUES (?, ?, ?, ?, ?)
        """, (nombre_cliente, telefono, servicio, fecha, hora))

        conexion.commit()
        conexion.close()

        return redirect(url_for("index"))

    return render_template("index.html")


@app.route("/eliminar/<int:id>")
def eliminar(id):
    """
    Ruta para eliminar una reserva segun su id.
    """
    conexion = conectar_db()
    conexion.execute("DELETE FROM reservas WHERE id = ?", (id,))
    conexion.commit()
    conexion.close()

    return redirect(url_for("index"))


# Se crea la base de datos automaticamente al iniciar la aplicacion
crear_base_datos()


if __name__ == "__main__":
    app.run(debug=True)
