from flask import Blueprint, render_template

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard")
def dashboard_home():
    return render_template("pages/dashboard.html")

# Agrega más rutas relacionadas con la administración aquí
