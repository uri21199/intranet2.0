from flask import Blueprint, render_template

notifications_bp = Blueprint("notifications", __name__)

@notifications_bp.route("/notifications")
def notifications_home():
    return render_template("pages/notifications.html")

# Agrega más rutas relacionadas con la notificationsistración aquí
