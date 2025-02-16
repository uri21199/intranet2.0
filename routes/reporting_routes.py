from flask import Blueprint, render_template, session, request, jsonify
from datetime import datetime
from sqlalchemy.orm import joinedload
from sqlalchemy import select, func
from models import Employee, RequestedDay, Training, TrainedEmployee, SalaryReceipt, Equipment, RoomReservation, DocumentVersion, SystemTicket, ChangeHistory, Role, EmployeeRole, Department, DayType, File
from config import SessionLocal
from sqlalchemy.orm import Session

reporting_bp = Blueprint("reporting", __name__)

@reporting_bp.route("/")
def reporting_home():
    return render_template("pages/reporting.html")


@reporting_bp.route("/generate_report", methods=["POST"])
def generate_report():
    try:
        data = request.get_json()  # Recibir los parámetros del formulario
        
        report_type = data.get("reportType")
        area = data.get("areaFilter")
        role = data.get("roleFilter")
        employee = data.get("employeeFilter")
        start_date = data.get("startDate")
        end_date = data.get("endDate")
        status = data.get("statusFilter")

        db: Session = SessionLocal()
        
        # Dependiendo del tipo de reporte, filtramos los datos
        if report_type == "employees_status":
            query = db.query(Employee)
            subquery = select(Department.name).where(Department.id == Employee.department_id).scalar_subquery()
            if area and area != "all":
                query = query.filter(Employee.department_id == area)
            if role and role != "all":
                query = query.join(EmployeeRole).filter(EmployeeRole.role_id == role)
            if employee and employee != "all":
                query = query.filter(Employee.id == employee)
            results = query.all()
            subquery = select(Department.name).where(Department.id == Employee.department_id).scalar_subquery()
            
            response = [{"name": f"{emp.first_name} {emp.last_name}", "CUIL": emp.tax_id, "Fecha de contratación": emp.hire_date, "Legajo": emp.record_number, "Email": emp.email, "Teléfono": emp.phone, "Dirección": f"{emp.address}, {emp.city}, {emp.state}", "Departamento": db.query(subquery).filter(Employee.id == emp.id).scalar()} for emp in results]

        elif report_type == "requested_days":
            subquery_employee = select(func.concat(Employee.first_name, " ", Employee.last_name)).where(Employee.id == RequestedDay.employee_id).scalar_subquery()
            subquery_day_type = select(DayType.name).where(DayType.id == RequestedDay.day_type_id).scalar_subquery()
            subquery_file_name = select(File.file_name).where(File.id == RequestedDay.file_id).scalar_subquery()
            subquery_file_path = select(File.file_path).where(File.id == RequestedDay.file_id).scalar_subquery()
            query = db.query(RequestedDay.id, subquery_employee.label("employee"), subquery_day_type.label("day_type"), RequestedDay.start_date, RequestedDay.end_date, RequestedDay.reason, RequestedDay.status, RequestedDay.created_at, subquery_file_name.label("file_name"), subquery_file_path.label("file_path"))
            if employee and employee != "all":
                query = query.filter(RequestedDay.employee_id == employee)
            if start_date:
                query = query.filter(RequestedDay.start_date >= start_date)
            if end_date:
                query = query.filter(RequestedDay.start_date <= end_date)
            results = query.all()

            response = [{
                "id": req.id,
                "Empleado": f"{req.employee}",
                "Tipo de Día": req.day_type,
                "Fecha de inicio": req.start_date,
                "Fecha de fin": req.end_date,
                "Motivo": req.reason,
                "Estado": req.status,
                "Fecha de creación": req.created_at,
                "Archivo": {
                    "Nombre": req.file_name if req.file_name else None,
                    "Ruta": req.file_path if req.file_path else None
                }
            } for req in results]


        else:
            return jsonify({"error": "Tipo de reporte no válido"}), 400

        return jsonify(response)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        db.close()
