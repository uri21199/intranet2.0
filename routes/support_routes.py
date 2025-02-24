from flask import Blueprint, request, jsonify, render_template, session
from sqlalchemy.orm import joinedload
from models import Employee, SystemTicket, TicketCategory, TicketSubcategory, TicketStatus, TicketUpdate    
from config import SessionLocal
from datetime import datetime, timedelta, timezone

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

@support_bp.route("/get_user_tickets", methods=["GET"])
def get_user_tickets():
    user_id = session.get("user_id")  # Obtener el usuario autenticado
    if not user_id:
        return jsonify({"error": "Usuario no autenticado"}), 401

    session_db = SessionLocal()
    try:
        # Obtener fecha límite de 15 días atrás
        fifteen_days_ago = datetime.now(timezone.utc) - timedelta(days=15)

        tickets = session_db.query(
            SystemTicket.id,
            TicketCategory.name.label("category"),
            TicketSubcategory.name.label("subcategory"),
            SystemTicket.description,
            TicketStatus.name.label("status"),
            SystemTicket.closed_at
        ).join(TicketCategory, TicketCategory.id == SystemTicket.category_id
        ).join(TicketSubcategory, TicketSubcategory.id == SystemTicket.subcategory_id
        ).join(TicketStatus, TicketStatus.id == SystemTicket.status_id
        ).filter(
            (SystemTicket.employee_id == user_id) &
            (
                (TicketStatus.name.in_(["Abierto", "En proceso", "Esperando usuario"]))
            )
        ).order_by(SystemTicket.created_at.desc()).all()

        ticket_list = [
            {
                "id": ticket.id,
                "category": ticket.category,
                "subcategory": ticket.subcategory,
                "description": ticket.description,
                "status": ticket.status
            }
            for ticket in tickets
        ]

        return jsonify(ticket_list)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    






    

@support_bp.route("/get_tickets", methods=["GET"])
def get_tickets():
    user_roles = session.get("roles", [])
    
    if "soporte tecnico" not in user_roles:
        return jsonify({"error": "Acceso no autorizado"}), 403

    session_db = SessionLocal()

    try:
        tickets = session_db.query(
            SystemTicket.id,
            TicketCategory.name.label("category"),
            TicketSubcategory.name.label("subcategory"),
            SystemTicket.description,
            TicketStatus.name.label("status"),
            Employee.first_name.label("assigned_to"),
            SystemTicket.created_at,
            SystemTicket.closed_at
        ).join(TicketCategory, TicketCategory.id == SystemTicket.category_id
        ).join(TicketSubcategory, TicketSubcategory.id == SystemTicket.subcategory_id
        ).join(TicketStatus, TicketStatus.id == SystemTicket.status_id
        ).outerjoin(Employee, Employee.id == SystemTicket.assigned_to
        ).filter(
            TicketStatus.name != "Cerrado"
        ).order_by(SystemTicket.id.desc()).all()

        ticket_list = [
            {
                "id": t.id,
                "category": t.category,
                "subcategory": t.subcategory,
                "description": t.description,
                "status": t.status,
                "assigned_to": t.assigned_to or "No asignado",
                "created_at": t.created_at.strftime("%Y-%m-%d %H:%M"),
                "closed_at": t.closed_at.strftime("%Y-%m-%d %H:%M") if t.closed_at else "No cerrado"
            }
            for t in tickets
        ]
        print(ticket_list)
        return jsonify(ticket_list)

    except Exception as e:
        print(f"Error en la consulta get_tickets: {str(e)}")
        return jsonify({"error": str(e)}), 500

    finally:
        session_db.close()


@support_bp.route("/get_ticket_filters", methods=["GET"])
def get_ticket_filters():
    session_db = SessionLocal()
    try:
        categories = session_db.query(TicketCategory.id, TicketCategory.name).all()
        statuses = session_db.query(TicketStatus.id, TicketStatus.name).all()

        filters = {
            "categories": [{"id": c.id, "name": c.name} for c in categories],
            "statuses": [{"id": s.id, "name": s.name} for s in statuses]
        }

        return jsonify(filters)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        session_db.close()
