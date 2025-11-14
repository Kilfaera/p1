from flask import Blueprint, render_template, request, redirect, url_for
from db.conexion import mysql

productos_bp = Blueprint("productos", __name__)


# LISTAR PRODUCTOS
@productos_bp.route("/productos")
def productos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos")
    data = cur.fetchall()
    return render_template("productos.html", productos=data)


# CREAR PRODUCTO
@productos_bp.route("/productos/agregar", methods=["POST"])
def agregar_producto():
    nombre = request.form["nombre"]
    precio = request.form["precio"]

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO productos (nombre, precio) VALUES (%s, %s)",
                (nombre, precio))
    mysql.connection.commit()
    return redirect(url_for("productos.productos"))


# CARGAR PRODUCTO PARA EDICIÓN
@productos_bp.route("/productos/editar/<int:id>")
def editar_producto(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos WHERE id = %s", (id,))
    producto = cur.fetchone()
    return render_template("productos_editar.html", producto=producto)


# ACTUALIZAR PRODUCTO
@productos_bp.route("/productos/actualizar/<int:id>", methods=["POST"])
def actualizar_producto(id):
    nombre = request.form["nombre"]
    precio = request.form["precio"]

    cur = mysql.connection.cursor()
    cur.execute("UPDATE productos SET nombre = %s, precio = %s WHERE id = %s",
                (nombre, precio, id))
    mysql.connection.commit()

    return redirect(url_for("productos.productos"))


# ELIMINAR PRODUCTO
@productos_bp.route("/productos/eliminar/<int:id>")
def eliminar_producto(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM productos WHERE id = %s", (id,))
    mysql.connection.commit()
    return redirect(url_for("productos.productos"))
