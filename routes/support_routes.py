from flask import Blueprint, render_template

support_bp = Blueprint("support", __name__)

@support_bp.route("/support")
def support_home():
    return render_template("pages/support.html")

# Agrega más rutas relacionadas con la administración aquí
