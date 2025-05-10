# db.session.bulk_save_objects(Lista dos json)

# id = 298

# src/controller/reembolso_controller.py

from flask import Blueprint, request, jsonify
from src.model.reembolso_model import Reembolso
from src.model import db
from flasgger import swag_from

bp_reembolsos = Blueprint('reembolso', __name__, url_prefix='/reembolso')

@bp_reembolsos.route('/solitacoes')
@swag_from('../docs/reembolso/listar_reembolsos.yml')
def visualizar_reembolso():
    reembolso = db.session.execute(
        db.select(Reembolso)
    ).scalar().all()
    
    if not reembolso:
        return jsonify({'mensagem': 'Nenhum reembolso não encontrado'}), 404
    
    return jsonify(reembolso.to_dict()), 200

@bp_reembolsos.route('/solicitacoes', methods=['POST'])
@swag_from('../docs/reembolso/solicitar_reembolso.yml')
def solicitar_reembolso():
    dados = request.get_json()
    
    novo_reembolso = Reembolso(
        colaborador=dados['colaborador'],
        empresa=dados['empresa'],
        num_prestacao=dados['num_prestacao'],
        descricao=dados.get('descricao', ''),
        data=dados.get('data'),
        tipo_reembolso=dados['tipo_reembolso'],
        centro_custo=dados['centro_custo'],
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