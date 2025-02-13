from flask import Blueprint, render_template, request, jsonify
from models.room_reservations import RoomReservation
from config import get_db
from sqlalchemy import and_
from sqlalchemy.orm import Session

rooms_bp = Blueprint("rooms", __name__)

@rooms_bp.route("/")
def rooms_home():
    return render_template("pages/rooms.html")

# Agrega más rutas relacionadas con la administración aquí
@rooms_bp.route("/create_reservation", methods=["POST"])
def create_reservation():
    data = request.get_json()
    db: Session = next(get_db()) 
    try:
        # Validar que no haya una reserva en el mismo horario y sala
        existing_reservation = db.query(RoomReservation).filter(
            RoomReservation.room_id == data["room_id"],
            RoomReservation.reservation_date == data["reservation_date"],
            and_(
                RoomReservation.start_time < data["end_time"],
                RoomReservation.end_time > data["start_time"]
            )
        ).first()
        
        if existing_reservation:
            return jsonify({"error": "La sala ya está reservada en este horario."}), 400
        new_reservation = RoomReservation(
            room_id=data["room_id"],
            reserved_by=data["reserved_by"],
            client_id=data.get("client_id"),  # Solo si es sala de reuniones
            use=data.get("use", "Capacitación"),
            justification=data.get("justification"),
            status="Pendiente",
            reservation_date=data["reservation_date"],
            start_time=data["start_time"],
            end_time=data["end_time"]
        )
        db.add(new_reservation)
        db.commit()
        return jsonify({"message": "Reserva creada exitosamente"}), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()