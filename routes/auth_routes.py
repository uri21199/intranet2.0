from flask import Blueprint, request, jsonify, session, redirect, url_for
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from config import get_db
from models.credentials import Credential
from models.employees import Employee
from models.departments import Department
from models.employee_roles import EmployeeRole
from models.roles import Role

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
        if credential.password == password:
            # Obtener el nombre del departamento
            department = db.query(Department).filter(Department.id == employee.department_id).first()
            department_name = department.name if department else None

            # Obtener los roles del usuario
            role_ids = db.query(EmployeeRole.role_id).filter(EmployeeRole.employee_id == employee.id).all()
            role_ids = [r[0] for r in role_ids]  # Convertir a una lista de IDs

            roles = db.query(Role.name).filter(Role.id.in_(role_ids)).all()
            role_names = [r[0] for r in roles]  # Convertir a lista de nombres

            # Guardar en sesión
            session['user_id'] = employee.id
            session['email'] = email
            session['first_name'] = employee.first_name
            session['last_name'] = employee.last_name
            session['department_id'] = employee.department_id
            session['department_name'] = department_name
            session['role_ids'] = role_ids
            session['roles'] = role_names
            print(f"Esto es el departamento y los roles: {session['department_name']} {session['roles']}")
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
