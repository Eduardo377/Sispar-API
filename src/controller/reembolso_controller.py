# db.session.bulk_save_objects(Lista dos json)

# id = 298

# src/controller/reembolso_controller.py

from flask import Blueprint, request, jsonify
from src.model.reembolso_model import Reembolso
from src.model import db
from sqlalchemy.sql import func
from flasgger import swag_from
from datetime import datetime

bp_reembolsos = Blueprint('reembolso', __name__, url_prefix='/reembolso')

@bp_reembolsos.route('/listar_reembolsos', methods=['GET'])
@swag_from('../docs/reembolso/listar_reembolsos.yml')
def visualizar_reembolso():
    reembolso = db.session.scalars(
        db.select(Reembolso)
    ).all()
    
    if not reembolso:
        return jsonify({'mensagem': 'Nenhum reembolso encontrado'}), 404
    
    return jsonify([r.to_dict() for r in reembolso]), 200

@bp_reembolsos.route('/solicitar_reembolso', methods=['POST'])
@swag_from('../docs/reembolso/solicitar_reembolso.yml')
def solicitar_reembolso():
    dados = request.get_json()
    
    novo_reembolso = Reembolso(
        colaborador=dados['colaborador'],
        empresa=dados['empresa'],
        num_prestacao=dados['num_prestacao'],
        descricao=dados.get('descricao', ''),
        data=dados.get('data') or datetime.now().date(),
        tipo_reembolso=dados['tipo_reembolso'],
        centro_custo=dados['c'],
        ordem_interna=dados.get('ordem_interna'),
        divisao=dados.get('divisao'),
        pep=dados.get('pep'),
        moeda=dados['moeda'],
        distancia_km=dados.get('distancia_km'),
        valor_km=dados.get('valor_km'),
        valor_faturado=dados['valor_faturado'],
        despesa=dados.get('despesa', 0),
        id_colaborador=dados['id_colaborador']
    )
    
    db.session.add(novo_reembolso)
    db.session.commit()
    
    return jsonify({'mensagem': 'Reembolso solicitado com sucesso'}), 201