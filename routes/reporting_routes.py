from flask import Blueprint, render_template

reporting_bp = Blueprint("reporting", __name__)

@reporting_bp.route("/reporting")
def reporting_home():
    return render_template("pages/reporting.html")

# Agrega más rutas relacionadas con la administración aquí
