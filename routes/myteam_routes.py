import csv
import pandas as pd
from flask import Blueprint, render_template, session, jsonify, request, send_file
from models.employees import Employee
from models.requested_days import RequestedDay
from models.day_types import DayType
from config import SessionLocal
from io import BytesIO

myteam_bp = Blueprint("myteam", __name__)

@myteam_bp.route("/")
def myteam_home():
    return render_template("pages/myteam.html")

# Agrega más rutas relacionadas con la administración aquí
@myteam_bp.route("/data", methods=["GET"])
def get_team_data():
    """Obtiene la lista de empleados del área y sus ausencias"""
    
    department_id = session.get("department_id")
    print(f"Department ID obtenido de sesión: {department_id}")  # Debug

    session_db = SessionLocal()
    employees = session_db.query(Employee).filter(Employee.department_id == department_id).all()
    print(f"Número de empleados en el departamento: {len(employees)}")  # Debug

    employee_data = []
    today_date = pd.Timestamp.today().date()  # Convertir a `datetime.date`

    # Rango de fechas para las ausencias del mes actual
    start_date_month = today_date.replace(day=1)  # Primer día del mes
    end_date_month = (start_date_month + pd.DateOffset(months=1) - pd.Timedelta(days=1)).date()  # Último día del mes

    for emp in employees:
        print(f"Procesando empleado: {emp.id} - {emp.first_name} {emp.last_name}")  # Debug

        absences = session_db.query(RequestedDay).filter(
            RequestedDay.employee_id == emp.id,
            RequestedDay.day_type_id.in_([1, 2, 4])  # Solo ausencia, estudio, vacaciones
        ).all()
        
        absences_count = len([a for a in absences if start_date_month <= a.start_date <= end_date_month])
        print(f"Empleado {emp.id}: Total ausencias en el mes actual: {absences_count}")  # Debug

        # Última ausencia antes de hoy
        last_absence = max([a.start_date for a in absences if a.start_date < today_date], default=None)
        
        # Próxima ausencia desde hoy en adelante
        next_absence = min([a.start_date for a in absences if a.start_date >= today_date], default=None)

        print(f"Empleado {emp.id}: Última ausencia: {last_absence}, Próxima ausencia: {next_absence}")  # Debug

        employee_data.append({
            "id": emp.id,
            "name": f"{emp.first_name} {emp.last_name}",
            "next_absence": next_absence.strftime("%d/%m/%Y") if next_absence else "-",
            "last_absence": last_absence.strftime("%d/%m/%Y") if last_absence else "-",
            "absence_count": absences_count
        })

    session_db.close()
    print("Datos generados para todos los empleados:", employee_data)  # Debug

    return jsonify(employee_data)


@myteam_bp.route("/export", methods=["GET"])
def export_team_data():
    """Exporta los datos de ausencias del equipo a CSV"""
    department_id = session.get("department_id")
    session_db = SessionLocal()
    
    employees = session_db.query(Employee).filter(Employee.department_id == department_id).all()
    data = []

    for emp in employees:
        absences = session_db.query(RequestedDay).filter(
            RequestedDay.employee_id == emp.id,
            RequestedDay.day_type_id.in_([1, 2, 4])
        ).all()
        
        for abs in absences:
            data.append([
                emp.first_name, emp.last_name, abs.start_date.strftime("%d/%m/%Y"),
                abs.end_date.strftime("%d/%m/%Y"), abs.reason
            ])

    session_db.close()
    
    df = pd.DataFrame(data, columns=["Nombre", "Apellido", "Fecha Inicio", "Fecha Fin", "Motivo"])
    output = BytesIO()
    df.to_csv(output, index=False, encoding="utf-8")
    output.seek(0)
    
    return send_file(output, mimetype="text/csv", as_attachment=True, download_name="ausencias_equipo.csv")

@myteam_bp.route("/absences-summary", methods=["GET"])
def get_absences_summary():
    """Devuelve el total de ausencias en la semana y en el mes para el área del jefe."""
    department_id = session.get("department_id")
    session_db = SessionLocal()
    
    today = pd.Timestamp.today()
    start_of_week = today - pd.Timedelta(days=today.weekday())  # Lunes de la semana actual
    end_of_week = start_of_week + pd.Timedelta(days=6)  # Domingo de la semana actual
    start_of_month = today.replace(day=1)  # Primer día del mes
    end_of_month = start_of_month + pd.DateOffset(months=1) - pd.Timedelta(days=1)  
    
    # Contar ausencias en la semana
    weekly_absences = session_db.query(RequestedDay).filter(
        RequestedDay.employee_id.in_(
            session_db.query(Employee.id).filter(Employee.department_id == department_id)
        ),
        RequestedDay.day_type_id.in_([1, 2, 4]),  # Solo ausencia, estudio, vacaciones
        RequestedDay.start_date >= start_of_week,
        RequestedDay.start_date <= end_of_week
    ).count()

    # Contar ausencias en el mes
    monthly_absences = session_db.query(RequestedDay).filter(
        RequestedDay.employee_id.in_(
            session_db.query(Employee.id).filter(Employee.department_id == department_id)
        ),
        RequestedDay.day_type_id.in_([1, 2, 4]),  # Solo ausencia, estudio, vacaciones
        RequestedDay.start_date >= start_of_month,
        RequestedDay.start_date <= end_of_month
    ).count()
    
    session_db.close()
    
    return jsonify({
        "weekly_absences": weekly_absences,
        "monthly_absences": monthly_absences
    })



@myteam_bp.route("/monthly-absences", methods=["GET"])
def get_monthly_absences():
    """Obtiene las ausencias del mes para los empleados del mismo departamento del jefe."""
    department_id = session.get("department_id")
    session_db = SessionLocal()

    today = pd.Timestamp.today()
    start_of_month = today.replace(day=1)  # Primer día del mes
    end_of_month = today.replace(day=28) + pd.Timedelta(days=4)  # Garantiza fin de mes

    absences = session_db.query(
        Employee.first_name, Employee.last_name,
        RequestedDay.start_date, RequestedDay.end_date,
        DayType.name.label("absence_type")
    ).join(RequestedDay, Employee.id == RequestedDay.employee_id) \
    .join(DayType, RequestedDay.day_type_id == DayType.id) \
    .filter(
        Employee.department_id == department_id,
        RequestedDay.day_type_id.in_([1, 2, 4]),  # Filtra ausencias, estudio y vacaciones
        RequestedDay.start_date >= start_of_month,
        RequestedDay.start_date <= end_of_month
    ).order_by(RequestedDay.start_date).all()

    session_db.close()

    absences_data = [{
        "name": f"{a.first_name} {a.last_name}",
        "start_date": a.start_date.strftime("%d/%m/%Y"),
        "absence_type": a.absence_type
    } for a in absences]

    return jsonify(absences_data)
