from flask import Blueprint, render_template, session, request, jsonify
from datetime import datetime
from sqlalchemy.orm import joinedload
from models import Employee, RequestedDay, Training, TrainedEmployee, SalaryReceipt, Equipment, RoomReservation, DocumentVersion, SystemTicket, ChangeHistory, Role
from config import SessionLocal

reporting_bp = Blueprint("reporting", __name__)

@reporting_bp.route("/")
def reporting_home():
    return render_template("pages/reporting.html")
