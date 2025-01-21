from flask import Blueprint

from .cadastro import cadastro_bp
from .atualizacao import atualizacao_bp
from .exclusao import exclusao_bp
from .anexo import anexo_bp
from .filtrar import filtrar_bp

def register_blueprints(app):
    app.register_blueprint(cadastro_bp)
    app.register_blueprint(atualizacao_bp)
    app.register_blueprint(exclusao_bp)
    app.register_blueprint(anexo_bp)
    app.register_blueprint(filtrar_bp)