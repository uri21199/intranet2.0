from flask import Blueprint, render_template

days_bp = Blueprint("days", __name__)

@days_bp.route("/days")
def days_home():
    return render_template("pages/days.html")

# Agrega más rutas relacionadas con la administración aquí
