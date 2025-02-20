from flask import Blueprint, render_template, jsonify, session, request
from config import get_db
from sqlalchemy.orm import Session, joinedload
from models import Room, Client, Role, Department, Employee, EmployeeRole, RequestedDay, DayType, Training, TrainedEmployee
from datetime import datetime, timedelta

employees_bp = Blueprint("employees", __name__)

@employees_bp.route("/")
def employees_home():
    return render_template("pages/employees.html")

# Agrega más rutas relacionadas con la administración aquí

@employees_bp.route("/get_requested_days", methods=["GET"])
def get_requested_days():
    employee_id = request.args.get("employee_id")
    
    if not employee_id:
        return jsonify({"error": "Falta employee_id"}), 400

    db: Session = next(get_db()) 

    try:
        today = datetime.today()
        start_date_filter = today - timedelta(days=15)
        end_date_filter = today + timedelta(days=30)

        days = (
            db.query(
                RequestedDay.start_date,
                RequestedDay.end_date,
                RequestedDay.reason,
                RequestedDay.status,
                DayType.name.label("day_type_name")  # Traemos el nombre del tipo de día
            )
            .join(DayType, RequestedDay.day_type_id == DayType.id)
            .filter(RequestedDay.employee_id == employee_id)
            .filter(RequestedDay.day_type_id != 3)  # Excluir Home Office
            .filter(RequestedDay.start_date >= start_date_filter)  # Últimos 15 días
            .filter(RequestedDay.start_date <= end_date_filter)  # Próximos 30 días
            .order_by(RequestedDay.start_date.desc())  # Ordenar por fecha descendente
            .all()
        )

        if not days:
            return jsonify({"message": "No hay días solicitados para este empleado."}), 200

        response = [
            {
                "day_type": day.day_type_name,
                "start_date": day.start_date.strftime('%d/%m/%Y'),
                "end_date": day.end_date.strftime('%d/%m/%Y') if day.start_date != day.end_date else "-",
                "status": day.status
            }
            for day in days
        ]

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        db.close()


@employees_bp.route("/get_home_office_days", methods=["GET"])
def get_home_office_days():
    employee_id = request.args.get("employee_id")

    if not employee_id:
        return jsonify({"error": "Falta employee_id"}), 400

    db: Session = next(get_db()) 

    try:
        today = datetime.today()
        start_date_filter = today - timedelta(days=15)
        end_date_filter = today + timedelta(days=30)

        home_office_days = (
            db.query(
                RequestedDay.start_date,
                RequestedDay.status,
                DayType.name.label("day_type_name")  # Relación con el tipo de día
            )
            .join(DayType, RequestedDay.day_type_id == DayType.id)
            .filter(RequestedDay.employee_id == employee_id)
            .filter(DayType.name == "home")  # Filtramos solo Home Office
            .filter(RequestedDay.start_date >= start_date_filter)  # Últimos 15 días
            .filter(RequestedDay.start_date <= end_date_filter)  # Próximos 30 días
            .order_by(RequestedDay.start_date.desc())  # Ordenar por fecha descendente
            .all()
        )

        if not home_office_days:
            return jsonify({"message": "No hay días de Home Office solicitados."}), 200

        response = [
            {
                "date": day.start_date.strftime('%d/%m/%Y'),
                "day_type": day.day_type_name,
                "status": day.status
            }
            for day in home_office_days
        ]

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        db.close()


@employees_bp.route("/get_trainings_done", methods=["GET"])
def get_trainings_done():
    employee_id = request.args.get("employee_id")
    
    if not employee_id:
        return jsonify({"error": "Falta employee_id"}), 400

    db: Session = next(get_db()) 

    try:
        trainings_done = (
            db.query(
                Training.name.label("training_name"),
                TrainedEmployee.attendance_date.label("training_date")
            )
            .join(Training, Training.id == TrainedEmployee.training_id)
            .filter(TrainedEmployee.employee_id == employee_id)
            .order_by(TrainedEmployee.attendance_date.desc())
            .all()
        )

        if not trainings_done:
            return jsonify({"message": "No hay capacitaciones registradas."}), 200

        response = [
            {
                "training_name": training.training_name,
                "training_date": training.training_date.strftime("%d/%m/%Y"),
            }
            for training in trainings_done
        ]

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        db.close()
