from flask import Blueprint, render_template

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin")
def admin_home():
    return render_template("pages/admin.html")

# Agrega más rutas relacionadas con la administración aquí
