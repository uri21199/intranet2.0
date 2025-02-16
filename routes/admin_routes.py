from flask import Blueprint, render_template, jsonify, session, request
from config import get_db
from sqlalchemy.orm import Session, joinedload
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




# Mapeo de roles a cargos
role_mapping = {
    "administrador general": "Gerencia",
    "jefe de area": "Jefe de X",  # Se reemplaza X dinámicamente
    "supervisor": "Supervisor de X",
    "capacitador": "Capacitador",
}

area_mapping = {
    "operaciones": "Operador",
    "claims": "Analista de facturación",
    "rrhh": "Recursos humanos",
    "reintegros": "Analista de reintegros",
    "sistemas": "Soporte en Sistemas",
    "analytics": "Analista de datos",
    "pagos": "Analista de pagos a proveedores",
    "bordereaux": "Analista de facturación",
    "comercial": "Comercial",
    "calidad": "Operador de calidad",
    "billing": "Analista de facturación",
    "maestranza": "Maestranza",
    "accounts": "Account Manager"
}


@admin_bp.route("/get_employee_info", methods=["GET"])
def get_employee_info():
    employee_id = request.args.get("employee_id")

    if not employee_id:
        print("⚠️ [ERROR] Falta el parámetro 'employee_id'")
        return jsonify({"error": "Falta employee_id"}), 400

    print(f"🔍 [INFO] Buscando información del empleado con ID: {employee_id}")

    db = next(get_db())

    try:
        # Buscar el empleado y traer los roles con join
        employee = (
            db.query(Employee)
            .options(joinedload(Employee.roles))  # Cargar roles
            .filter(Employee.id == employee_id)
            .first()
        )

        if not employee:
            print(f"❌ [ERROR] No se encontró el empleado con ID: {employee_id}")
            return jsonify({"error": "Empleado no encontrado"}), 404

        print(f"✅ [INFO] Empleado encontrado: {employee.first_name} {employee.last_name}")

        # Obtener los roles del empleado
        roles = [role.name for role in employee.roles] if employee.roles else ["Empleado"]
        print(f"🎭 [INFO] Roles del empleado: {roles}")

        # Determinar el cargo basado en los roles
        cargo = "Empleado"
        encontrado_en_roles = False  # Bandera para saber si ya se asignó cargo por roles

        for role_name in roles:
            role_name = role_name.lower()

            if "supervisor" in role_name:
                cargo = f"Supervisor de {employee.department.name if employee.department else 'N/A'}"
                print(f"🎯 [INFO] Se encontró rol jerárquico: {cargo}. Deteniendo búsqueda.")
                encontrado_en_roles = True
                break  # 🔴 Se encontró un rol prioritario, no sigue buscando.

            elif "jefe de area" in role_name:
                cargo = f"Jefe de {employee.department.name if employee.department else 'N/A'}"
                print(f"🎯 [INFO] Se encontró rol jerárquico: {cargo}. Deteniendo búsqueda.")
                encontrado_en_roles = True
                break  # 🔴 Se encontró un rol prioritario, no sigue buscando.

            elif role_name in role_mapping:
                cargo = role_mapping[role_name]
                print(f"🔍 [INFO] Cargo asignado por mapeo de roles: {cargo}")
                encontrado_en_roles = True
                break  # 🔴 Asigna el primer cargo válido en role_mapping.

        # Si no se encontró un cargo en roles, asignar cargo según el área
        if not encontrado_en_roles:
            department_name = employee.department.name.lower() if employee.department else "sin asignar"
            cargo = area_mapping.get(department_name, "Empleado")  # Default a "Empleado" si el área no está en el mapeo
            print(f"🏢 [INFO] Cargo asignado por área: {cargo}")

        print(f"✅ [INFO] Cargo final asignado: {cargo}")


        # Obtener el departamento (manejo seguro de None)
        department_name = employee.department.name if employee.department else "Sin asignar"
        print(f"🏢 [INFO] Departamento: {department_name}")

        # Construir la respuesta
        response = {
            "id": employee.id,
            "name": f"{employee.first_name} {employee.last_name}",
            "department": department_name,
            "cargo": cargo,
            "roles": roles  # Agregar los roles en la respuesta
        }

        print("✅ [INFO] Respuesta generada con éxito:", response)
        return jsonify(response)

    except Exception as e:
        print(f"🔥 [ERROR] Excepción en get_employee_info: {str(e)}")
        return jsonify({"error": "Error interno del servidor"}), 500

    finally:
        db.close()
        print("🔄 [INFO] Conexión a la base de datos cerrada.")
