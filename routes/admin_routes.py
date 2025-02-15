from flask import Blueprint, render_template, jsonify, session, request
from config import get_db
from sqlalchemy.orm import Session
from models import Room, Client, Role, Department, Employee, EmployeeRole

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/")
def admin_home():
    return render_template("pages/admin.html")

@admin_bp.route("/get_user_info", methods=["GET"])
def get_user_info():
    user_data = {
        "id": session.get("user_id"),
        "roles": session.get("roles", []),
        "department_id": session.get("department_id"),
        "department_name": session.get("department_name")
    }
    return jsonify(user_data)


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

@admin_bp.route("/get_areas", methods=["GET"])
def get_areas():
    db: Session = next(get_db())
    try:
        areas = db.query(Department).all()
        response = [{"id": area.id, "name": area.name} for area in areas]
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@admin_bp.route("/get_roles", methods=["GET"])
def get_roles():
    db: Session = next(get_db())
    try:
        roles = db.query(Role).all()
        response = [{"id": role.id, "name": role.name} for role in roles]
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@admin_bp.route("/get_employees", methods=["GET"])
def get_employees():
    area_id = request.args.get("area_id")
    role_id = request.args.get("role_id")

    db: Session = next(get_db())
    try:
        query = db.query(Employee)

        if area_id:
            query = query.filter(Employee.department_id == area_id)
        if role_id:
            query = query.join(EmployeeRole).filter(EmployeeRole.role_id == role_id)

        employees = query.all()
        response = [{"id": emp.id, "name": f"{emp.first_name} {emp.last_name}"} for emp in employees]
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


