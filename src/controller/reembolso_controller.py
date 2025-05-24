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
            date=dados.get('date'),
            expense_type=dados['expense_type'],
            cost_center=dados['cost_center'],
            internal_order=dados.get('internal_order'),
            div=dados.get('div'),
            pep=dados.get('pep'),
            currency=dados['currency'],
            distance=dados.get('distance'),
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
        elif 'name' not in dados_reembolso:
            reembolso.name =reembolso.name
        if 'company' in dados_reembolso:
            reembolso.company = dados_reembolso['company']
        elif 'company' not in dados_requisicao:
            reembolso.company = reembolso.company
        if 'date' in dados_reembolso:
            reembolso.date = dados_reembolso['date']
        elif 'date' not in dados_reembolso:
            reembolso.date = reembolso.date
        if 'expense_type' in dados_reembolso:
            reembolso.expense_type = dados_reembolso['expense_type']
        elif 'expense_type' not in dados_reembolso:
            reembolso.expense_type = reembolso.expense_type
        if 'cost_center' in dados_reembolso:
            reembolso.cost_center = dados_reembolso['cost_center']
        elif 'cost_center' not in dados_reembolso:
            reembolso.cost_center = reembolso.cost_center
        if 'internal_order' in dados_reembolso:
            reembolso.internal_order = dados_reembolso['internal_order']
        elif 'internal_order' not in dados_reembolso:
            reembolso.internal_order = reembolso.internal_order
        if 'div' in dados_reembolso:
            reembolso.div = dados_reembolso['div']
        elif 'div' not in dados_reembolso:
            reembolso.div = reembolso.div
        if 'pep' in dados_reembolso:
            reembolso.pep = dados_reembolso['pep']
        elif 'pep' not in dados_reembolso:
            reembolso.pep = reembolso.pep
        if 'currency' in dados_reembolso:
            reembolso.currency = dados_reembolso['currency']
        elif 'currency' not in dados_reembolso:
            reembolso.currency = reembolso.currency
        if 'distance' in dados_reembolso:
            reembolso.distance = dados_reembolso['distance']
        elif 'distance' not in dados_reembolso:
            reembolso.distance = reembolso.distance
        if 'value_km' in dados_reembolso:
            reembolso.value_km = dados_reembolso['value_km']
        elif 'value_km' not in dados_reembolso:
            reembolso.value_km = reembolso.value_km
        if 'value_billed' in dados_reembolso:
            reembolso.value_billed = dados_reembolso['value_billed']
        elif 'value_billed' not in dados_reembolso:
            reembolso.value_billed = reembolso.value_billed
        if 'expense' in dados_reembolso:
            reembolso.expense = dados_reembolso['expense']
        elif 'expense' not in dados_reembolso:
            reembolso.expense = reembolso.expense
        if 'status' in dados_reembolso:
            reembolso.status = dados_reembolso['status']
        elif 'status' not in dados_reembolso:
            reembolso.status = reembolso.status
                
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
                
@bp_reembolsos.route('/mockar', methods=['POST'])
@swag_from('../docs/reembolso/mockar_reembolso.yml')
def popular_rembolsos():
    # mock_reembolso = request.get_json()  # Pega o conteúdo da requisição
    
    mock = [
                        {
                            "name": "Marina Gomes de Almeida",
                            "company": "WSS002",
                            "installment_number": 328451,
                            "date": "2025-02-12",
                            "expense_type": "Desp. de viagem comercial",
                            "cost_center": "1100110003 - DIR COMERCIAL SP",
                            "internal_order": "0012",
                            "div": "003",
                            "pep": "003",
                            "currency": "BRL",
                            "distance": "232Km",
                            "value_km": "0.68",
                            "value_billed": 157.76,
                            "expense": 35.40,
                            "id_colaborador": 2
                        },
                        {
                            "name": "Carlos Eduardo Ferreira",
                            "company": "WSS003",
                            "installment_number": 328452,
                            "date": "2025-03-08",
                            "expense_type": "Desp. de viagem administrativa",
                            "cost_center": "1100110005 - SUPRIMENTOS RJ",
                            "internal_order": "0010",
                            "div": "001",
                            "pep": "002",
                            "currency": "BRL",
                            "distance": "150Km",
                            "value_km": "0.65",
                            "value_billed": 97.50,
                            "expense": 22.00,
                            "id_colaborador": 3
                        },
                        {
                            "name": "Juliana Alves Martins",
                            "company": "WSS004",
                            "installment_number": 328453,
                            "date": "2025-01-19",
                            "expense_type": "Desp. de viagem técnica",
                            "cost_center": "1100110010 - ENGENHARIA PROJETOS MTZ",
                            "internal_order": "0008",
                            "div": "002",
                            "pep": "004",
                            "currency": "BRL",
                            "distance": "350Km",
                            "value_km": "0.67",
                            "value_billed": 234.50,
                            "expense": 48.30,
                            "id_colaborador": 4
                        },
                        {
                            "name": "André Souza Lima",
                            "company": "WSS005",
                            "installment_number": 328454,
                            "date": "2025-04-05",
                            "expense_type": "Desp. de visita técnica",
                            "cost_center": "1100110006 - OPERACOES NORDESTE",
                            "internal_order": "0006",
                            "div": "004",
                            "pep": "001",
                            "currency": "BRL",
                            "distance": "415Km",
                            "value_km": "0.65",
                            "value_billed": 269.75,
                            "expense": 38.15,
                            "id_colaborador": 5
                        },
                        {
                            "name": "Fernanda Carvalho Ribeiro",
                            "company": "WSS006",
                            "installment_number": 328455,
                            "date": "2025-01-27",
                            "expense_type": "Desp. de inspeção",
                            "cost_center": "1100110007 - QUALIDADE E SEGURANÇA",
                            "internal_order": "0015",
                            "div": "002",
                            "pep": "002",
                            "currency": "BRL",
                            "distance": "278Km",
                            "value_km": "0.66",
                            "value_billed": 183.48,
                            "expense": 33.80,
                            "id_colaborador": 6
                        },
                        {
                            "name": "Renato Lima Oliveira",
                            "company": "WSS007",
                            "installment_number": 328456,
                            "date": "2025-02-03",
                            "expense_type": "Desp. de suporte técnico",
                            "cost_center": "1100110011 - TI SUPORTE RJ",
                            "internal_order": "0009",
                            "div": "001",
                            "pep": "003",
                            "currency": "BRL",
                            "distance": "196Km",
                            "value_km": "0.70",
                            "value_billed": 137.20,
                            "expense": 27.50,
                            "id_colaborador": 7
                        },
                        {
                            "name": "Tatiane Barros da Luz",
                            "company": "WSS008",
                            "installment_number": 328457,
                            "date": "2025-03-11",
                            "expense_type": "Desp. de viagem administrativa",
                            "cost_center": "1100110009 - ADMINISTRAÇÃO CENTRAL",
                            "internal_order": "0014",
                            "div": "005",
                            "pep": "001",
                            "currency": "BRL",
                            "distance": "320Km",
                            "value_km": "0.69",
                            "value_billed": 220.80,
                            "expense": 36.90,
                            "id_colaborador": 8
                        },
                        {
                            "name": "Roberto Silva Costa",
                            "company": "WSS009",
                            "installment_number": 328458,
                            "date": "2025-01-23",
                            "expense_type": "Desp. de operação técnica",
                            "cost_center": "1100110012 - MANUTENÇÃO RJ",
                            "internal_order": "0011",
                            "div": "003",
                            "pep": "004",
                            "currency": "BRL",
                            "distance": "390Km",
                            "value_km": "0.68",
                            "value_billed": 265.20,
                            "expense": 42.35,
                            "id_colaborador": 9
                        },
                        {
                            "name": "Priscila Dias Nogueira",
                            "company": "WSS010",
                            "installment_number": 328459,
                            "date": "2025-04-01",
                            "expense_type": "Desp. de supervisão",
                            "cost_center": "1100110013 - SUPERVISÃO SUL",
                            "internal_order": "0007",
                            "div": "002",
                            "pep": "003",
                            "currency": "BRL",
                            "distance": "410Km",
                            "value_km": "0.65",
                            "value_billed": 266.50,
                            "expense": 45.90,
                            "id_colaborador": 10
                        }
                    ]
    mock_reembolso = mock # Verifica se o corpo da requisição está vazio, se sim, usa a lista mockada
    # Lista de colaboradores mockados
    if not mock_reembolso:
        return jsonify({"mensagem": "Nenhum reembolso mockado encontrado!"}), 400
    for item in mock_reembolso:
        reembolso = Reembolso(
            name=item["name"],
            company=item["company"],
            installment_number=item["installment_number"],
            date=item["date"],
            expense_type=item["expense_type"],
            cost_center=item["cost_center"],
            internal_order=item["internal_order"],
            div=item["div"],
            pep=item["pep"],
            currency=item["currency"],
            distance=item["distance"],
            value_km=item["value_km"],
            value_billed=item["value_billed"],
            expense=item["expense"],
            id_colaborador=item["id_colaborador"]
        )
        db.session.add(reembolso)
    db.session.commit()
    return jsonify({"mensagem": "✅ Reembolsos cadastrados com sucesso!"}), 200