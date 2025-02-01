from flask import Flask
from routes import register_blueprints

app = Flask(__name__)

# Registrar las rutas organizadas
register_blueprints(app)

if __name__ == "__main__":
    app.run(debug=True)
