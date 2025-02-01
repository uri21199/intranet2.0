from flask import Blueprint, render_template

settings_bp = Blueprint("settings", __name__)

@settings_bp.route("/settings")
def settings_home():
    return render_template("pages/settings.html")

# Agrega más rutas relacionadas con la administración aquí
