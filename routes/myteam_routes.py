from flask import Blueprint, render_template

myteam_bp = Blueprint("myteam", __name__)

@myteam_bp.route("/myteam")
def myteam_home():
    return render_template("pages/myteam.html")

# Agrega más rutas relacionadas con la administración aquí
