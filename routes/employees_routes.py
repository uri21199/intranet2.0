from flask import Blueprint, render_template

employees_bp = Blueprint("employees", __name__)

@employees_bp.route("/employees")
def employees_home():
    return render_template("pages/employees.html")

# Agrega más rutas relacionadas con la administración aquí
