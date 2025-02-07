from flask import Blueprint, request, jsonify, session, redirect, url_for
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from config import get_db
from models.credentials import Credential
from models.employees import Employee

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message": "Email y contraseña son obligatorios"}), 400

    db: Session = next(get_db())  # Obtener una sesión de la base de datos

    try:
        # Buscar el empleado por email
        employee = db.query(Employee).filter(Employee.email == email).first()

        if not employee:
            print("❌ Usuario no encontrado en la base de datos.")
            return jsonify({"message": "Usuario no encontrado"}), 404

        # Buscar credenciales con el employee_id obtenido
        credential = db.query(Credential).filter(Credential.employee_id == employee.id).first()

        if not credential:
            print("❌ No hay credenciales registradas para este usuario.")
            return jsonify({"message": "Credenciales no registradas"}), 404
        # Comparar contraseña en texto plano
        print(f"🔍 Contraseña ingresada: {password}")
        print(f"🔍 Contraseña en BD: {credential.password}")
        # Comparar contraseña en texto plano
        if credential.password == password:
            session['user_id'] = employee.id
            session['email'] = email
            print(f"✅ Login exitoso para {email}, redirigiendo a /dashboard")
            return jsonify({"message": "Login exitoso", "redirect": url_for('dashboard.dashboard_home')}), 200
        else:
            print("❌ Contraseña incorrecta.")
            return jsonify({"message": "Contraseña incorrecta"}), 401
    except SQLAlchemyError as e:
        import traceback
        print("❌ ERROR COMPLETO:")
        print(traceback.format_exc())  # Muestra el error completo en la terminal
        return jsonify({"message": "Error en la base de datos", "error": str(e)}), 500
    finally:
        db.close()

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Sesión cerrada"}), 200
