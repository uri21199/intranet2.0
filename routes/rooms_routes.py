from flask import Blueprint, render_template, request, jsonify, session
from models.room_reservations import RoomReservation
from config import get_db
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session
from datetime import datetime

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

@rooms_bp.route("/get_reservations", methods=["GET"])
def get_reservations():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"message": "No autenticado"}), 401

    room_id = request.args.get("room_id")
    status = request.args.get("status")

    db: Session = next(get_db()) 
    try:
        query = db.query(RoomReservation).filter(RoomReservation.reserved_by == user_id)

        if room_id:
            query = query.filter(RoomReservation.room_id == room_id)
        if status:
            query = query.filter(RoomReservation.status == status)

        results = query.all()
        response = [{
            "id": r.id,
            "room_name": r.room.name,
            "reservation_date": r.reservation_date.strftime('%Y-%m-%d'),
            "start_time": r.start_time.strftime('%H:%M'),
            "end_time": r.end_time.strftime('%H:%M'),
            "status": r.status
        } for r in results]

        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@rooms_bp.route("/update_reservation", methods=["POST"])
def update_reservation():
    if "user_id" not in session:
        return jsonify({"message": "No autenticado"}), 401

    data = request.json
    reservation_id = data.get("reservation_id")
    new_date = data.get("new_date")
    new_start_time = data.get("new_start_time")
    new_end_time = data.get("new_end_time")

    db: Session = next(get_db()) 
    try:
        # Buscar la reserva a actualizar
        reservation = db.query(RoomReservation).filter(
            RoomReservation.id == reservation_id,
            RoomReservation.status == "Pendiente"
        ).first()

        if not reservation:
            return jsonify({"message": "No se puede editar esta reserva"}), 400

        # Convertir las fechas y horas a objetos datetime
        new_start_time_parsed = datetime.strptime(new_start_time, "%H:%M").time()
        new_end_time_parsed = datetime.strptime(new_end_time, "%H:%M").time()
        new_date_parsed = datetime.strptime(new_date, "%Y-%m-%d").date()

        # Validar que no haya otra reserva en la misma sala, fecha y horario
        existing_reservation = db.query(RoomReservation).filter(
            RoomReservation.room_id == reservation.room_id,
            RoomReservation.reservation_date == new_date_parsed,
            RoomReservation.id != reservation_id,  # Excluir la reserva actual
            or_(
                and_(
                    RoomReservation.start_time < new_end_time_parsed,
                    RoomReservation.end_time > new_start_time_parsed
                )
            )
        ).first()

        if existing_reservation:
            return jsonify({"message": "Ya existe una reserva en este horario"}), 400

        # Si pasa las validaciones, actualizar la reserva
        reservation.reservation_date = new_date_parsed
        reservation.start_time = new_start_time_parsed
        reservation.end_time = new_end_time_parsed

        db.commit()
        return jsonify({"message": "Reserva actualizada correctamente"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@rooms_bp.route("/delete_reservation", methods=["POST"])
def delete_reservation():
    if "user_id" not in session:
        return jsonify({"message": "No autenticado"}), 401

    data = request.json
    reservation_id = data.get("reservation_id")

    db: Session = next(get_db()) 
    try:
        reservation = db.query(RoomReservation).filter(
            RoomReservation.id == reservation_id,
            RoomReservation.status == "Pendiente"
        ).first()

        if not reservation:
            return jsonify({"message": "No se puede eliminar esta reserva"}), 400

        db.delete(reservation)
        db.commit()
        return jsonify({"message": "Reserva eliminada correctamente"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
