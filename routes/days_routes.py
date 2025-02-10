from flask import Blueprint, request, jsonify, session, render_template
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from config import get_db
from models.requested_days import RequestedDay
from models.day_types import DayType
from datetime import datetime


days_bp = Blueprint("days", __name__)

@days_bp.route("/days")
def days_home():
    return render_template("pages/days.html")

# Agrega más rutas relacionadas con la administración aquí

# Definir el blueprint para las rutas relacionadas con días
days_request_bp = Blueprint("days_request", __name__)

@days_request_bp.route("/days_request", methods=["POST"])
def days_request():
    if 'user_id' not in session:
        return jsonify({"message": "No autenticado"}), 401
    
    data = request.json
    employee_id = session['user_id']
    day_type_id = data.get("day_type_id")
    fechas = data.get("fechas", [])
    reason = data.get("reason", "")
    asistencia = data.get("asistencia", None)
    
    db: Session = next(get_db())
    try:
        # Verificar si el tipo de día existe
        day_type = db.query(DayType).filter(DayType.id == day_type_id).first()
        if not day_type:
            return jsonify({"message": "Tipo de día inválido"}), 400

        nuevas_solicitudes = []
        for fecha in fechas:
            start_date = datetime.strptime(fecha, "%Y-%m-%d").date()
            end_date = start_date if day_type.name != "vacaciones" else datetime.strptime(data.get("end_date"), "%Y-%m-%d").date()
            
            # Verificar si ya existe una solicitud igual
            existing_request = db.query(RequestedDay).filter(
                RequestedDay.employee_id == employee_id,
                RequestedDay.day_type_id == day_type_id,
                RequestedDay.start_date == start_date
            ).first()
            
            if existing_request:
                return jsonify({"message": "Ya existe una solicitud para la fecha: " + fecha}), 400
            
            nueva_solicitud = RequestedDay(
                employee_id=employee_id,
                day_type_id=day_type_id,
                start_date=start_date,
                end_date=end_date,
                reason=reason if day_type.name in ["ausencia", "estudio"] else None,
                status="Pendiente",
                file_id=None
            )
            nuevas_solicitudes.append(nueva_solicitud)
        
        db.add_all(nuevas_solicitudes)
        db.commit()
        return jsonify({"message": "Días solicitados exitosamente"}), 200
    
    except SQLAlchemyError as e:
        db.rollback()
        return jsonify({"message": "Error en la base de datos", "error": str(e)}), 500
    finally:
        db.close()
