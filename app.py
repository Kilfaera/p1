from flask import Flask, render_template
from config import Config
from db.conexion import init_app

from routes.productos import productos_bp
from routes.facturas import facturas_bp
from routes.inventario import inventario_bp



app = Flask(__name__)
app.config.from_object(Config)

init_app(app)

app.register_blueprint(inventario_bp)
app.register_blueprint(productos_bp)
app.register_blueprint(facturas_bp)

@app.route("/")
def index():
    return render_template("index.html")



if __name__ == "__main__":
    app.run(debug=True)
