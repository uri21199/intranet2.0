from flask import Blueprint, render_template, jsonify
from config import get_db
from sqlalchemy.orm import Session
from models.rooms import Room
from models.clients import Client

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin")
def admin_home():
    return render_template("pages/admin.html")

@admin_bp.route("/get_rooms", methods=["GET"])
def get_rooms():
    db: Session = next(get_db()) 
    try:
        rooms = db.query(Room).all()
        print("🔍 Salas obtenidas de la BD:", rooms)  # DEBUG
        response = [{"id": room.id, "name": room.name} for room in rooms]
        print("📤 Respuesta enviada:", response)  # DEBUG
        return jsonify(response)
    except Exception as e:
        print("❌ Error en get_rooms:", str(e))  # DEBUG
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

# Ruta para obtener todos los clientes
@admin_bp.route("/get_clients", methods=["GET"])
def get_clients():
    db: Session = next(get_db()) 
    try:
        clients = db.query(Client).all()
        print("🔍 Clientes obtenidos de la BD:", clients)  # DEBUG

        # Convertimos cada objeto en un diccionario
        response = [{"id": client.id, "name": str(client.name)} for client in clients]
        
        print("📤 Respuesta enviada:", response)  # DEBUG
        return jsonify(response)
    except Exception as e:
        print("❌ Error en get_clients:", str(e))  # DEBUG
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
