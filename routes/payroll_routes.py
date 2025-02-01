from flask import Blueprint, render_template

payroll_bp = Blueprint("payroll", __name__)

@payroll_bp.route("/payroll")
def payroll_home():
    return render_template("pages/payroll.html")

# Agrega más rutas relacionadas con la administración aquí
