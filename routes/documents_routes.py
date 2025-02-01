from flask import Blueprint, render_template

documents_bp = Blueprint("documents", __name__)

@documents_bp.route("/documents")
def documents_home():
    return render_template("pages/documents.html")

# Agrega más rutas relacionadas con la administración aquí
