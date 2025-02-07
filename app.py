from flask import Flask
from routes import register_blueprints

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_segura'  # Cambia esto por una clave segura
# Registrar las rutas organizadas
register_blueprints(app)

if __name__ == "__main__":
    app.run(debug=True)
