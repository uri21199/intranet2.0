from flask import Blueprint, render_template

trainings_bp = Blueprint("trainings", __name__)

@trainings_bp.route("/trainings")
def trainings_home():
    return render_template("pages/trainings.html")

# Agrega más rutas relacionadas con la administración aquí
