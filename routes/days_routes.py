from flask import Blueprint, request, jsonify, session, render_template
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from config import get_db
from models.requested_days import RequestedDay
from models.day_types import DayType
from models.files import File
from datetime import datetime, timedelta
import os
from werkzeug.utils import secure_filename

days_bp = Blueprint("days", __name__)

@days_bp.route("/")
def days_home():
    return render_template("pages/days.html")

@days_bp.route("/days_request", methods=["POST"])
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



@days_bp.route("/get_days", methods=["GET"])
def get_days():
    if 'user_id' not in session:
        return jsonify({"message": "No autenticado"}), 401
    
    user_id = session['user_id']
    day_type = request.args.get("day_type")
    motivo = request.args.get("motivo")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    
    db: Session = next(get_db())
    try:
        query = db.query(RequestedDay).filter(
            RequestedDay.employee_id == user_id,
            RequestedDay.status != "Suspendida"  # Excluir fechas con estado Suspendida
        )
        
        # Filtrar fechas 1 mes antes y 1 mes después
        today = datetime.today().date()
        min_date = today - timedelta(days=30)
        max_date = today + timedelta(days=30)
        query = query.filter(RequestedDay.start_date.between(min_date, max_date))
        
        # Aplicar filtros opcionales
        if day_type:
            query = query.filter(RequestedDay.day_type_id == day_type)
        if motivo:
            query = query.filter(RequestedDay.reason == motivo)
        if start_date and end_date:
            query = query.filter(RequestedDay.start_date.between(start_date, end_date))
        
        results = query.all()
        response = [{
            "id": r.id,
            "day_type": r.day_type_id,
            "start_date": r.start_date.strftime('%Y-%m-%d'),
            "end_date": r.end_date.strftime('%Y-%m-%d') if r.end_date else r.start_date.strftime('%Y-%m-%d'),
            "reason": r.reason,
            "status": r.status,
            "file": r.file_id
        } for r in results]
        
        return jsonify(response), 200
    except SQLAlchemyError as e:
        return jsonify({"message": "Error en la base de datos", "error": str(e)}), 500
    finally:
        db.close()

@days_bp.route("/update_day", methods=["POST"])
def update_day():
    if 'user_id' not in session:
        return jsonify({"message": "No autenticado"}), 401

    data = request.json
    day_id = data.get("day_id")
    new_date = data.get("new_date")

    db: Session = next(get_db())
    try:
        day_request = db.query(RequestedDay).filter(
            RequestedDay.id == day_id,
            RequestedDay.status == "Pendiente"
        ).first()

        if not day_request:
            return jsonify({"message": "No se puede editar esta solicitud"}), 400

        # Obtener el tipo de día
        day_type = db.query(DayType).filter(DayType.id == day_request.day_type_id).first()

        if not day_type:
            return jsonify({"message": "Tipo de día inválido"}), 400

        # Convertir la nueva fecha a datetime
        new_date_parsed = datetime.strptime(new_date, "%Y-%m-%d").date()

        # Si el tipo de día NO es "vacaciones", end_date debe ser igual a start_date
        if day_type.name.lower() in ["ausencia", "estudio", "home office"]:
            day_request.start_date = new_date_parsed
            day_request.end_date = new_date_parsed  # Asegurar que se actualiza también
        else:
            # Para vacaciones, actualizar solo start_date si existe end_date
            if day_request.end_date and new_date_parsed > day_request.end_date:
                return jsonify({"message": "La fecha de inicio no puede ser mayor a la fecha de fin"}), 400
            day_request.start_date = new_date_parsed

        db.commit()
        return jsonify({"message": "Solicitud actualizada correctamente"}), 200

    except SQLAlchemyError as e:
        db.rollback()
        return jsonify({"message": "Error en la base de datos", "error": str(e)}), 500
    finally:
        db.close()

@days_bp.route("/delete_day", methods=["POST"])
def delete_day():
    if 'user_id' not in session:
        return jsonify({"message": "No autenticado"}), 401
    
    data = request.json
    day_id = data.get("day_id")
    
    db: Session = next(get_db())
    try:
        day_request = db.query(RequestedDay).filter(RequestedDay.id == day_id, RequestedDay.status == "Pendiente").first()
        
        if not day_request:
            return jsonify({"message": "No se puede eliminar esta solicitud"}), 400
        
        day_request.status = "Suspendida"
        db.commit()
        return jsonify({"message": "Solicitud eliminada correctamente"}), 200
    except SQLAlchemyError as e:
        db.rollback()
        return jsonify({"message": "Error en la base de datos", "error": str(e)}), 500
    finally:
        db.close()





UPLOAD_FOLDER = "uploads/"  # Carpeta donde se guardarán los archivos
ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png", "docx"}  # Extensiones permitidas

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@days_bp.route("/upload_file", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    if file is None or file.filename == "":
        return jsonify({"message": "No se envió ningún archivo válido"}), 400

    request_id = request.form.get("request_id")
    if not request_id or not request_id.isdigit():
        return jsonify({"message": "ID de solicitud inválido"}), 400

    db = next(get_db())

    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Guardar en la tabla 'files'
        new_file = File(
            file_name=filename,
            file_path=file_path,
            request_id=int(request_id)
        )
        db.add(new_file)
        db.commit()

        # Obtener el ID del archivo recién guardado
        file_id = new_file.id

        # Actualizar 'file_id' en la tabla 'requested_days'
        day_request = db.query(RequestedDay).filter(RequestedDay.id == request_id).first()
        if day_request:
            day_request.file_id = file_id
            db.commit()

        return jsonify({"message": "Archivo subido y asociado correctamente"}), 200

    except Exception as e:
        db.rollback()
        return jsonify({"message": "Error al subir archivo", "error": str(e)}), 500

    finally:
        db.close()
