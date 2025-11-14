from flask import Blueprint, render_template, request, redirect, url_for
from db.conexion import mysql

inventario_bp = Blueprint("inventario", __name__)


# LISTAR INVENTARIO
@inventario_bp.route("/inventario")
def inventario():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT i.id, p.nombre, i.cantidad
        FROM inventario i
        JOIN productos p ON i.id_producto = p.id
    """)
    data = cur.fetchall()
    return render_template("inventario.html", inventario=data)


# CARGAR FORMULARIO PARA AGREGAR STOCK
@inventario_bp.route("/inventario/agregar")
def inventario_agregar():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre FROM productos")
    productos = cur.fetchall()
    return render_template("inventario_agregar.html", productos=productos)


# INSERTAR STOCK
@inventario_bp.route("/inventario/crear", methods=["POST"])
def inventario_crear():
    id_producto = request.form["producto"]
    cantidad = request.form["cantidad"]

    cur = mysql.connection.cursor()

    # Verificamos si el producto ya tiene un registro de inventario
    cur.execute("SELECT id FROM inventario WHERE id_producto = %s", (id_producto,))
    existe = cur.fetchone()

    if existe:
        cur.execute("UPDATE inventario SET cantidad = cantidad + %s WHERE id_producto = %s",
                    (cantidad, id_producto))
    else:
        cur.execute("INSERT INTO inventario (id_producto, cantidad) VALUES (%s, %s)",
                    (id_producto, cantidad))

    mysql.connection.commit()
    return redirect(url_for("inventario.inventario"))


# EDITAR STOCK
@inventario_bp.route("/inventario/editar/<int:id>")
def editar_inventario(id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT i.id, p.nombre, i.cantidad, i.id_producto
        FROM inventario i
        JOIN productos p ON i.id_producto = p.id
        WHERE i.id = %s
    """, (id,))
    registro = cur.fetchone()

    return render_template("inventario_editar.html", inventario=registro)


# ACTUALIZAR STOCK
@inventario_bp.route("/inventario/actualizar/<int:id>", methods=["POST"])
def actualizar_inventario(id):
    cantidad = request.form["cantidad"]

    cur = mysql.connection.cursor()
    cur.execute("UPDATE inventario SET cantidad = %s WHERE id = %s",
                (cantidad, id))
    mysql.connection.commit()

    return redirect(url_for("inventario.inventario"))


# ELIMINAR REGISTRO DE INVENTARIO
@inventario_bp.route("/inventario/eliminar/<int:id>")
def eliminar_inventario(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM inventario WHERE id = %s", (id,))
    mysql.connection.commit()

    return redirect(url_for("inventario.inventario"))
