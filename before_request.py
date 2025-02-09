from flask import session, g, request, redirect, url_for
from sqlalchemy.orm import Session
from config import get_db
from models.employees import Employee
from models.departments import Department
from models.roles import Role
from models.employee_roles import EmployeeRole


# Definir qué roles pueden ver cada bloque
SIDEBAR_BLOCKS = [
    {"name": "Administración", "icon": "admin_panel_settings", "url": "#", "roles": ["administrador general"]},
    {"name": "Dashboard", "icon": "dashboard", "url": "#", "roles": ["operador"]},
    {"name": "Días", "icon": "edit_calendar", "url": "#", "roles": ["operador"]},
    {"name": "Documentos", "icon": "description", "url": "#", "roles": ["operador"]},
    {"name": "Empleados", "icon": "groups", "url": "#", "roles": ["administrador general", "recursos humanos"]},
    {"name": "Mi equipo", "icon": "group", "url": "#", "roles": ["jefe de area"]},
    {"name": "Notificaciones", "icon": "notifications", "url": "#", "roles": ["operador"]},
    {"name": "Recibo de sueldo", "icon": "receipt_long", "url": "#", "roles": ["operador"]},
    {"name": "Reportes", "icon": "download", "url": "#", "roles": ["analista de datos"]},
    {"name": "Salas", "icon": "room_preferences", "url": "#", "roles": ["organizador de reuniones"]},
    {"name": "Configuración", "icon": "settings", "url": "#", "roles": ["operador"]},
    {"name": "Soporte", "icon": "desktop_cloud_stack", "url": "#", "roles": ["operador"]},
    {"name": "Encuestas", "icon": "mood", "url": "#", "roles": ["operador"]},
    {"name": "Capacitaciones", "icon": "school", "url": "#", "roles": ["operador"]},
    # Agregá más bloques según los roles que existan
]

def before_request_handler():
    print("🔥 before_request ejecutado!")
    if 'user_id' not in session:
        if request.endpoint and request.endpoint not in ['auth.login', 'static']:
            return redirect(url_for('auth.login'))  # Redirige a login si no está autenticado

    else:
        db: Session = next(get_db())

        try:
            # Obtener información del usuario desde la base de datos para actualizar la sesión
            employee = db.query(Employee).filter(Employee.id == session['user_id']).first()
            if employee:
                session['first_name'] = employee.first_name
                session['last_name'] = employee.last_name
                session['email'] = employee.email
                session['department_id'] = employee.department_id

                # Obtener el nombre del departamento
                department = db.query(Department).filter(Department.id == employee.department_id).first()
                session['department_name'] = department.name if department else None

                # Obtener roles del usuario
                role_ids = db.query(EmployeeRole.role_id).filter(EmployeeRole.employee_id == employee.id).all()
                role_ids = [r[0] for r in role_ids]  # Convertir en lista de IDs

                roles = db.query(Role.name).filter(Role.id.in_(role_ids)).all()
                session['roles'] = [r[0] for r in roles]  # Convertir a lista de nombres
                print(f"esto son los roles guardados en before_request: {session['roles']}")
                # Hacer los datos accesibles en `g` para el resto de la app
                g.user = {
                    "id": session['user_id'],
                    "first_name": session['first_name'],
                    "last_name": session['last_name'],
                    "email": session['email'],
                    "department_id": session['department_id'],
                    "department_name": session['department_name'],
                    "roles": session['roles']
                }
            # Filtrar los bloques que el usuario puede ver según sus roles
            g.sidebar_blocks = [block for block in SIDEBAR_BLOCKS if any(role in session['roles'] for role in block["roles"])]
        except Exception as e:
            print(f"Error en before_request: {e}")
            session.clear()  # Limpiar la sesión en caso de error
            return redirect(url_for('auth.login'))  # Redirigir a login

        finally:
            db.close()
