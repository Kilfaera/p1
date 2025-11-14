from flask import Blueprint, render_template, request
from db.conexion import mysql

facturas_bp = Blueprint("facturas", __name__)

@facturas_bp.route("/facturas")
def facturas():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT f.id, f.fecha, p.nombre, f.cantidad, 
                   (f.cantidad * p.precio) AS total
                   FROM facturas f
                   JOIN productos p ON f.id_producto = p.id""")
    data = cur.fetchall()
    return render_template("facturas.html", facturas=data)

@facturas_bp.route("/facturas/crear", methods=["POST"])
def crear_factura():
    id_producto = request.form["producto"]
    cantidad = request.form["cantidad"]

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO facturas (id_producto, cantidad) VALUES (%s, %s)",
                (id_producto, cantidad))
    # Restar del inventario
    cur.execute("UPDATE inventario SET cantidad = cantidad - %s WHERE id_producto = %s",
            (cantidad, id_producto))

    mysql.connection.commit()
    return "Factura creada exitosamente"
