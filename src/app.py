# RESPONSAVEL POR CRIAR A APLICAÇÃO

from flask import Flask
from src.controller.colaborador_controller import bp_colaborador
from src.model import db
from config import Config

def create_app():
    
    app = Flask(__name__)
    app.register_blueprint(bp_colaborador)
    app.config.from_object(Config)
    db.init_app(app) # Inicializa o banco de dados com a aplicação Flask
    
    with app.app_context():
        db.create_all() # Cria todas as tabelas no banco de dados
    
    return app