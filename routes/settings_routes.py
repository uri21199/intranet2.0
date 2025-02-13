from flask import Blueprint, render_template, jsonify, session, request
from werkzeug.security import generate_password_hash, check_password_hash
from models.employees import Employee
from models.credentials import Credential
from config import get_db
from sqlalchemy.orm import Session

settings_bp = Blueprint("settings", __name__)

@settings_bp.route("/")
def settings_home():
    return render_template("pages/settings.html")

# Agrega más rutas relacionadas con la administración aquí
@settings_bp.route("/update", methods=["POST"])
def update_settings():
    db = next(get_db())  # Obtener la sesión de la base de datos
    user_id = session.get("user_id")
    
    print(f"🟡 USER_ID: {user_id}")  # 📌 Verificar el usuario en la sesión

    if not user_id:
        print("❌ Error: No hay usuario en sesión.")
        return jsonify({"message": "Debes iniciar sesión para realizar cambios."}), 403

    employee = db.query(Employee).filter(Employee.id == user_id).first()
    credential = db.query(Credential).filter(Credential.employee_id == user_id).first()

    if not employee or not credential:
        print("❌ Error: No se encontró información del usuario.")
        return jsonify({"message": "No se encontró información del usuario."}), 404

    try:
        data = request.get_json()
        print("📥 Datos recibidos:", data)  # 📌 Ver los datos enviados por el cliente

        # Validar cambio de contraseña
        # Validar cambio de contraseña sin hashing
        updated = False

        if "newPassword" in data and data["newPassword"]:
            if credential.password != data["currentPassword"]:  # Comparación simple en lugar de check_password_hash
                print("❌ Error: La contraseña actual no es correcta.")
                return jsonify({"message": "La contraseña actual no es correcta."}), 400

            if data["newPassword"] != data["confirmPassword"]:
                print("❌ Error: Las nuevas contraseñas no coinciden.")
                return jsonify({"message": "Las nuevas contraseñas no coinciden."}), 400

            credential.password = data["newPassword"]  # Guardar la nueva contraseña en texto plano
            updated = True
            print("✅ Contraseña actualizada.")


        # Validar y actualizar otros datos
        if "email" in data and data["email"] != employee.email:
            employee.email = data["email"]
            updated = True
        if "phone" in data and data["phone"] != employee.phone:
            employee.phone = data["phone"]
            updated = True
        if "state" in data and data["state"] != employee.state:
            employee.state = data["state"]
            updated = True
        if "city" in data and data["city"] != employee.city:
            employee.city = data["city"]
            updated = True
        if "address" in data and data["address"] != employee.address:
            employee.address = data["address"]
            updated = True

        if updated:
            db.commit()  # ✅ Guardar cambios en la base de datos
            print("✅ Datos del usuario actualizados correctamente.")
            return jsonify({"message": "Los cambios han sido guardados exitosamente."}), 200

        print("⚠️ No se realizaron cambios.")
        return jsonify({"message": "No se realizaron cambios."}), 200
    
    except Exception as e:
        print("❌ Error inesperado:", e)
        db.rollback()  # Revertir cambios si ocurre un error
        return jsonify({"message": "Error interno del servidor."}), 500




@settings_bp.route("/user-info", methods=["GET"])
def get_user_info():
    user_id = session.get("user_id")
    print(f"USER_ID en sesión: {user_id}")  # Depuración
    db: Session = next(get_db())
    if not user_id:
        print("⚠️ No hay user_id en la sesión.")
        return jsonify({"message": "Debes iniciar sesión para ver esta información."}), 403

    employee = db.query(Employee).filter(Employee.id == session['user_id']).first()
    
    if not employee:
        print("⚠️ No se encontró un empleado con ese ID.")
        return jsonify({"message": "No se encontró la información del usuario."}), 404

    print(f"✅ Usuario encontrado: {employee.email}")

    user_data = {
        "email": employee.email,
        "phone": employee.phone,
        "state": employee.state,
        "city": employee.city,
        "address": employee.address
    }

    return jsonify(user_data), 200
