import os
from flask import Blueprint, request, jsonify, session
from werkzeug.utils import secure_filename
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from config import get_db
from models.requested_days import RequestedDay
from models.files import File

# Configuración de la carpeta de almacenamiento
UPLOAD_FOLDER = "static/files"
ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}

upload_bp = Blueprint("upload", __name__)

# Función para verificar si el archivo es permitido
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route("/upload_file", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"message": "No se envió ningún archivo"}), 400

    file = request.files["file"]
    request_id = request.form.get("request_id")

    if file.filename == "":
        return jsonify({"message": "Nombre de archivo vacío"}), 400

    if not allowed_file(file.filename):
        return jsonify({"message": "Extensión de archivo no permitida"}), 400

    db: Session = next(get_db())

    try:
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        new_file = File(
            file_name=filename,
            file_path=file_path,
            request_id=request_id
        )
        db.add(new_file)
        db.commit()

        return jsonify({"message": "Archivo subido correctamente"}), 200

    except Exception as e:
        db.rollback()
        return jsonify({"message": "Error al subir archivo", "error": str(e)}), 500

    finally:
        db.close()