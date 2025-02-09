from flask import session, g, request, redirect, url_for
from sqlalchemy.orm import Session
from config import get_db
from models.employees import Employee
from models.departments import Department
from models.roles import Role
from models.employee_roles import EmployeeRole

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

        except Exception as e:
            print(f"Error en before_request: {e}")
            session.clear()  # Limpiar la sesión en caso de error
            return redirect(url_for('auth.login'))  # Redirigir a login

        finally:
            db.close()
