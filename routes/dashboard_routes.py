from flask import Blueprint, render_template

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
def dashboard_home():
    print("✅ Accediendo al dashboard")
    return render_template("pages/dashboard.html")
