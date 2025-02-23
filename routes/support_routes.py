from flask import Blueprint, request, jsonify, render_template, session
from sqlalchemy.orm import joinedload
from models.system_tickets import SystemTicket
from models.ticket_categories import TicketCategory
from models.ticket_subcategories import TicketSubcategory
from models.ticket_status import TicketStatus
from config import SessionLocal

support_bp = Blueprint("support", __name__)

@support_bp.route("/")
def support_home():
    return render_template("pages/support.html")

# Agrega más rutas relacionadas con la administración aquí
@support_bp.route("/get_ticket_categories", methods=["GET"])
def get_ticket_categories():
    session_roles = session.get("roles", [])  # Obtener roles de la sesión
    print(session_roles, "ESTOS SON LOS ROLES")
    session_db = SessionLocal()
    try:
        # Filtrar categorías según los roles del usuario
        allowed_categories = session_db.query(TicketCategory).filter(
            (TicketCategory.id == 4) & (any(role in session_roles for role in ["recursos humanos", "soporte tecnico", "gestor de clientes", "jefe de area"])) |
            (TicketCategory.id.in_([5, 6])) & ("soporte tecnico" in session_roles) |
            (TicketCategory.id.notin_([4, 5, 6]))  # Permitir otras categorías a todos
        ).all()

        categories = [{"id": cat.id, "name": cat.name} for cat in allowed_categories]
        return jsonify({"categories": categories})

    finally:
        session_db.close()


@support_bp.route("/get_ticket_subcategories", methods=["GET"])
def get_ticket_subcategories():
    category_id = request.args.get("category_id")
    session_roles = session.get("roles", [])  # Obtener los roles de la sesión

    session_db = SessionLocal()
    try:
        if category_id == "4":
            if "gestor_clientes" in session_roles:
                subcategories = session_db.query(TicketSubcategory).filter(TicketSubcategory.id.in_([16, 19])).all()
            else:
                subcategories = session_db.query(TicketSubcategory).filter(TicketSubcategory.category_id == 4).all()
        else:
            subcategories = session_db.query(TicketSubcategory).filter(TicketSubcategory.category_id == category_id).all()

        subcategories_list = [{"id": sub.id, "name": sub.name} for sub in subcategories]
        return jsonify({"subcategories": subcategories_list})

    finally:
        session_db.close()


@support_bp.route("/create_ticket", methods=["POST"])
def create_ticket():
    data = request.json
    category_id = data.get("category_id")
    subcategory_id = data.get("subcategory_id")
    description = data.get("description")

    if not category_id or not subcategory_id:
        return jsonify({"error": "Faltan datos obligatorios."}), 400

    session_db = SessionLocal()
    try:
        # Obtener el usuario autenticado (simulación)
        user_id = session['user_id']
        default_status = session_db.query(TicketStatus).filter_by(name="Abierto").first()

        new_ticket = SystemTicket(
            employee_id=user_id,
            category_id=category_id,
            subcategory_id=subcategory_id,
            description=description,
            assigned_to=123,
            status_id=default_status.id if default_status else None
        )

        session_db.add(new_ticket)
        session_db.commit()
        return jsonify({"success": True})

    except Exception as e:
        session_db.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        session_db.close()