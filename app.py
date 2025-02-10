from flask import Flask
from routes import register_blueprints
from before_request import before_request_handler

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_segura'  # Asegúrate de que sea única y segura

# Registrar las rutas organizadas 
app.before_request(before_request_handler)
register_blueprints(app)

# Agregar el manejador de before_request
print("📍 Flask URL Map:", app.url_map)


if __name__ == "__main__":
    app.run(debug=True)
