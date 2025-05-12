# db.session.bulk_save_objects(Lista dos json)

# id = 298

# src/controller/reembolso_controller.py

from flask import Blueprint, request, jsonify
from src.model.reembolso_model import Reembolso
from src.model import db
from sqlalchemy.sql import func
from flasgger import swag_from

bp_reembolsos = Blueprint('reembolso', __name__, url_prefix='/reembolso')
@bp_reembolsos.route('/solicitar_reembolso', methods=['POST'])
@swag_from('../docs/reembolso/solicitar_reembolso.yml')
def solicitar_reembolso():
    dados = request.get_json()
    
    try:
        novo_reembolso = Reembolso(
            name=dados['name'],
            company=dados['company'],
            installment_number=dados['installment_number'],
            description=dados.get('description', ''),
            date=dados.get('date'),
            expense_type=dados['expense_type'],
            cost_center=dados['cost_center'],
            internal_order=dados.get('internal_order'),
            div=dados.get('div'),
            pep=dados.get('pep'),
            currency=dados['currency'],
            distance_km=dados.get('distance_km'),
            value_km=dados.get('value_km'),
            value_billed=dados['value_billed'],
            expense=dados.get('expense', 0),
            id_colaborador=dados['id_colaborador']
        )
        
        db.session.add(novo_reembolso)
        db.session.commit()
        return jsonify({'mensagem': 'Reembolso solicitado com sucesso'}), 201
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'erro': 'Erro ao solicitar reembolso'}), 400
    
@bp_reembolsos.route('/listar_reembolsos', methods=['GET'])
@swag_from('../docs/reembolso/listar_reembolsos.yml')
def visualizar_reembolso():
    reembolso = db.session.scalars(
        db.select(Reembolso)
    ).all()
    
    if not reembolso:
        return jsonify({'mensagem': 'Nenhum reembolso encontrado'}), 404
    
    return jsonify([r.to_dict() for r in reembolso]), 200

# Endereco/reembolso/atualizar/<id_reembolso>
@bp_reembolsos.route('/atualizar/<int:id_reembolso>', methods=['PUT'])
@swag_from('../docs/reembolso/atualizar_reembolso.yml')
def atualizar_dados_do_reembolso(id_reembolso):
    dados_reembolso = request.get_json()

    try:
        reembolso = db.session.query(Reembolso).get(id_reembolso) # Buscando o reembolso pelo id

        if not reembolso:
            return jsonify({'erro': 'Reembolso não encontrado'}), 404
        if 'name' in dados_reembolso:
            reembolso.name = dados_reembolso['name']
        if 'company' in dados_reembolso:
            reembolso.company = dados_reembolso['company']
        if 'description' in dados_reembolso:
            reembolso.description = dados_reembolso['description']
        if 'date' in dados_reembolso:
            reembolso.date = dados_reembolso['date']
        if 'expense_type' in dados_reembolso:
            reembolso.expense_type = dados_reembolso['expense_type']
        if 'cost_center' in dados_reembolso:
            reembolso.cost_center = dados_reembolso['cost_center']
        if 'internal_order' in dados_reembolso:
            reembolso.internal_order = dados_reembolso['internal_order']
        if 'div' in dados_reembolso:
            reembolso.div = dados_reembolso['div']
        if 'pep' in dados_reembolso:
            reembolso.pep = dados_reembolso['pep']
        if 'currency' in dados_reembolso:
            reembolso.currency = dados_reembolso['currency']
        if 'distance_km' in dados_reembolso:
            reembolso.distance_km = dados_reembolso['distance_km']
        if 'value_km' in dados_reembolso:
            reembolso.value_km = dados_reembolso['value_km']
        if 'value_billed' in dados_reembolso:
            reembolso.value_billed = dados_reembolso['value_billed']
        if 'expense' in dados_reembolso:
            reembolso.expense = dados_reembolso['expense']
        if 'status' in dados_reembolso:
            reembolso.status = dados_reembolso['status'] 
                
        db.session.commit()
        return jsonify({'mensagem': 'Dados do reembolso atualizados com sucesso'}), 200
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'erro': 'Erro ao atualizar reembolso.'}), 400
    
# Endereco/reembolso/deletar/<id_reembolso>
@bp_reembolsos.route('/deletar/<int:id_reembolso>', methods=['DELETE'])
@swag_from('../docs/reembolso/deletar_reembolso.yml')
def deletar_reembolso(id_reembolso):
    reembolso = db.session.query(Reembolso).get(id_reembolso) # Buscando o reembolso pelo id
    
    try:
        if not reembolso:
            return jsonify({'erro': 'Reembolso não encontrado'}), 404
    
        db.session.delete(reembolso)
        db.session.commit()
        return jsonify({'mensagem': 'Reembolso deletado com sucesso'}), 200
    
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'erro': 'Erro ao deletar reembolso'}), 400