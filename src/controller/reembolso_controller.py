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
@bp_reembolsos.route('/solicitar_reembolso', methods=['POST'])
@swag_from('../docs/reembolso/solicitar_reembolso.yml')
def solicitar_reembolso():
    dados = request.get_json()
    
    try:
        novo_reembolso = Reembolso(
            colaborador=dados['colaborador'],
            empresa=dados['empresa'],
            num_prestacao=dados['num_prestacao'],
            descricao=dados.get('descricao', ''),
            data=dados.get('data') or datetime.now().date(),
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

# Endereco/colaborador/atualizar/1
@bp_reembolsos.route('/atualizar/<int:id_reembolso>', methods=['PUT'])
@swag_from('../docs/reembolso/atualizar_reembolso.yml')
def atualizar_dados_do_reembolso(id_reembolso):
    dados_reembolso = request.get_json()

    try:
        reembolso = db.session.query(Reembolso).get(id_reembolso) # Buscando o colaborador pelo id

        if not reembolso:
            return jsonify({'erro': 'Reembolso não encontrado'}), 404
        if 'colaborador' in dados_reembolso:
            reembolso.colaborador = dados_reembolso['colaborador']
        if 'empresa' in dados_reembolso:
            reembolso.empresa = dados_reembolso['empresa']
        if 'descricao' in dados_reembolso:
            reembolso.descricao = dados_reembolso['descricao']
        if 'data' in dados_reembolso:
            reembolso.data = dados_reembolso['data']
        if 'tipo_reembolso' in dados_reembolso:
            reembolso.tipo_reembolso = dados_reembolso['tipo_reembolso']
        if 'centro_custo' in dados_reembolso:
            reembolso.centro_custo = dados_reembolso['centro_custo']
        if 'ordem_interna' in dados_reembolso:
            reembolso.ordem_interna = dados_reembolso['ordem_interna']
        if 'divisao' in dados_reembolso:
            reembolso.divisao = dados_reembolso['divisao']
        if 'pep' in dados_reembolso:
            reembolso.pep = dados_reembolso['pep']
        if 'moeda' in dados_reembolso:
            reembolso.moeda = dados_reembolso['moeda']
        if 'distancia_km' in dados_reembolso:
            reembolso.distancia_km = dados_reembolso['distancia_km']
        if 'valor_km' in dados_reembolso:
            reembolso.valor_km = dados_reembolso['valor_km']
        if 'valor_faturado' in dados_reembolso:
            reembolso.valor_faturado = dados_reembolso['valor_faturado']
        if 'despesa' in dados_reembolso:
            reembolso.despesa = dados_reembolso['despesa']
        if 'status' in dados_reembolso:
            reembolso.status = dados_reembolso['status'] 
                
        db.session.commit()
        return jsonify({'mensagem': 'Dados do reembolso atualizados com sucesso'}), 200
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'erro': 'Erro ao atualizar reembolso.'}), 400
    
@bp_reembolsos.route('/deletar/<int:id_reembolso>', methods=['DELETE'])
@swag_from('../docs/reembolso/deletar_reembolso.yml')
def deletar_reembolso(id_reembolso):
    reembolso = db.session.query(Reembolso).get(id_reembolso) # Buscando o colaborador pelo id
    
    try:
        if not reembolso:
            return jsonify({'erro': 'Reembolso não encontrado'}), 404
    
        db.session.delete(reembolso)
        db.session.commit()
        return jsonify({'mensagem': 'Reembolso deletado com sucesso'}), 200
    
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'erro': 'Erro ao deletar reembolso'}), 400