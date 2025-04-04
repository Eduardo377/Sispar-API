from flask import Blueprint, request, jsonify

from src.model import db
from src.model.colaborador_model import Colaborador

# 

bp_colaborador = Blueprint('colaborador', __name__, url_prefix='/colaborador')

@bp_colaborador.route('/pegar-dados')

def pegar_dados():
    dados = [
            {'nome': 'Karynne Moreira', 'cargo': 'CEO', 'cracha': '010101'},
            {'nome': 'Samuel Silverio', 'cargo': 'CTO', 'cracha': '74512'},
            {'nome': 'Thales Reis', 'cargo': 'Desenvolvedor Back-end Java', 'cracha': '14523'},
            {'nome': 'Eduardo Gomes', 'cargo': 'DevOps', 'cracha': '78412'},
            {'nome': 'Gabriel Silvano', 'cargo': 'Desenvolvedor Front-end React', 'cracha': '96523'},
            {'nome': 'Suelen Braga', 'cargo': 'Infra', 'cracha': '251473'}
        ]
        
    return dados

@bp_colaborador.route('/cadastrar', methods=['POST'])

def cadastrar_novo_colaborador():
    dados_requisicao = request.get_json()

    novo_colaborador = Colaborador(
        nome=dados_requisicao['nome'],
        email=dados_requisicao['email'],
        senha=dados_requisicao['senha'],
        cargo=dados_requisicao['cargo'],
        salario=dados_requisicao['salario']
    )
    
    db.session.add(novo_colaborador) # Adiciona o novo colaborador à sessão do banco de dados
    db.session.commit() # Salva as alterações no banco de dados
    
    return jsonify( {'mensagem': 'Dado cadastrado com sucesso!'} )

@bp_colaborador.route('/atualizar/<int:id_colaborador>', methods=['PUT'])
def atualizar_dados_do_colaborador(id_colaborador):
    dados_requisicao = request.get_json()
    
    for colaborador in dados:
        if colaborador['id'] == id_colaborador:
            colaborador_encontrado = colaborador
            break
        if 'nome' in dados_requisicao: 
            colaborador_encontrado['nome'] = dados_requisicao['nome'] 
        if 'cargo' in dados_requisicao: 
            colaborador_encontrado['cargo'] = dados_requisicao['cargo']
            
    return jsonify({'mensagem': 'Dados do colaborador atualizados com sucesso!'}), 200