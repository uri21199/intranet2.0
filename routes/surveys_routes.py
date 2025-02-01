from flask import Blueprint, render_template

surveys_bp = Blueprint("surveys", __name__)

@surveys_bp.route("/surveys")
def surveys_home():
    return render_template("pages/surveys.html")

# Agrega más rutas relacionadas con la administración aquí
