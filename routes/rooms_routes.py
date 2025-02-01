from flask import Blueprint, render_template

rooms_bp = Blueprint("rooms", __name__)

@rooms_bp.route("/rooms")
def rooms_home():
    return render_template("pages/rooms.html")

# Agrega más rutas relacionadas con la administración aquí
