from flask import Blueprint

# Importar los blueprints existentes
from .admin_routes import admin_bp
from routes.auth_routes import auth_bp
from .dashboard_routes import dashboard_bp
from .days_routes import days_bp
from .documents_routes import documents_bp
from .employees_routes import employees_bp
from .myteam_routes import myteam_bp
from .notifications_routes import notifications_bp
from .payroll_routes import payroll_bp
from .reporting_routes import reporting_bp
from .rooms_routes import rooms_bp
from .support_routes import support_bp
from .surveys_routes import surveys_bp
from .trainings_routes import trainings_bp
from .settings_routes import settings_bp
from .main_routes import main_bp  # Agregamos la nueva ruta

# Función para registrar todos los blueprints
def register_blueprints(app):
    app.register_blueprint(main_bp)  # Agregamos el blueprint de index
    app.register_blueprint(auth_bp, url_prefix='/auth') # Login/logout
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')  # Dashboard
    app.register_blueprint(days_bp)
    app.register_blueprint(documents_bp)
    app.register_blueprint(employees_bp)
    app.register_blueprint(myteam_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(payroll_bp)
    app.register_blueprint(reporting_bp)
    app.register_blueprint(rooms_bp)
    app.register_blueprint(support_bp)
    app.register_blueprint(surveys_bp)
    app.register_blueprint(trainings_bp)
    app.register_blueprint(settings_bp)
