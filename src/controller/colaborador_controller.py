from flask import Blueprint, request, jsonify
from src.model.colaborador_model import Colaborador
from src.model import db
from src.security.security import hash_senha, checar_senha
from flasgger import swag_from
from sqlalchemy.exc import IntegrityError

# request -> trabalha com as requisições. Pega o conteúdo da requisição
# jsonify -> Trabalha com as respostas. Converte um dado em Json

bp_colaborador = Blueprint('colaborador', __name__, url_prefix='/colaborador')

# Endereco/colaborador/login
@bp_colaborador.route('/login', methods=['POST'])
@swag_from('../docs/colaborador/login_colaborador.yml')
def login():
    dados_requisicao = request.get_json()
    
    email = dados_requisicao.get('email')
    senha = dados_requisicao.get('senha')
    
    if not email or not senha:
        return jsonify({'mensagem': 'Todos os dados precisam ser preenchidos'}), 400
    
    # SELECT * FROM [TABELA]
    colaborador = db.session.execute(
        db.select(Colaborador).where(Colaborador.email == email)
    ).scalar() # -> A linha de informação OU None
    
    print('*'*100)
    print(f'dado: {colaborador} é do tipo {type(colaborador)}')
    print('*'*100)
    
    if not colaborador:
        return jsonify({'mensagem': 'Usuario não encontrado'}), 404
    
    colaborador = colaborador.to_dict()
    
    print('*'*100)
    print(f'dado: {colaborador} é do tipo {type(colaborador)}')
    print('*'*100)
    
    if email == colaborador.get('email') and checar_senha(senha, colaborador.get('senha')):
        return jsonify({'mensagem': 'Login realizado com sucesso'}), 200
    else:
        return jsonify({'mensagem': 'Credenciais invalidas'}), 400
    
# Endereco/colaborador/cadastrar/1
@bp_colaborador.route('/cadastrar', methods=['POST'])
@swag_from('../docs/colaborador/cadastrar_colaborador.yml')
def cadastrar_novo_colaborador(): 
    
    dados_requisicao = request.get_json()
    
    try:
        senha_criptografada = hash_senha(dados_requisicao['senha'])
        novo_colaborador = Colaborador(
            nome=dados_requisicao['nome'],
            email=dados_requisicao['email'],
            senha=senha_criptografada,
            cargo=dados_requisicao['cargo'],
            salario=dados_requisicao['salario']
        )
    
#   INSERT INTO tb_colaborador (nome, email, senha, cargo, salario) VALUES (VALOR1,VALOR2,VALOR3,VALOR4,VALOR5)
        db.session.add(novo_colaborador)
        db.session.commit() # Essa linha executa a query
        return jsonify( {'mensagem': 'Dado cadastrado com sucesso'}), 201
    except Exception as e:
        print(f"Erro: {e}")  # ou logar com logger
        return jsonify({'erro': 'Erro ao cadastrar colaborador'}), 400

# Endereco/colaborador/listar
@bp_colaborador.route('/listar', methods=['GET'])
@swag_from('../docs/colaborador/listar_colaboradores.yml')
def pegar_dados_todos_colaboradores():
    
    colaboradores = db.session.execute(
        db.select(Colaborador)
    ).scalars().all()
    
#                       expressão                   item        iteravel
    colaboradores = [ colaborador.all_data() for colaborador in colaboradores ]
    
    return jsonify(colaboradores), 200

# Endereco/colaborador/atualizar/1
@bp_colaborador.route('/atualizar/<int:id_colaborador>', methods=['PUT'])
@swag_from('../docs/colaborador/atualizar_colaborador.yml')
def atualizar_dados_do_colaborador(id_colaborador):
    
    dados_requisicao = request.get_json()
    
    try:
        colaborador = db.session.query(Colaborador).get(id_colaborador)

        if not colaborador:
            return jsonify({'erro': 'Colaborador não encontrado'}), 404
        
        if 'nome' in dados_requisicao:
            colaborador.nome = dados_requisicao['nome']
        if 'email' in dados_requisicao:
            colaborador.email = dados_requisicao['email']
        if 'senha' in dados_requisicao:
            senha_criptografada = hash_senha(dados_requisicao['senha'])
            colaborador.senha = senha_criptografada
        if 'cargo' in dados_requisicao:
            colaborador.cargo = dados_requisicao['cargo']
        if 'salario' in dados_requisicao:
            colaborador.salario = dados_requisicao['salario']
            
        db.session.add(colaborador)
        db.session.commit()

        return jsonify({'mensagem': 'Dados do colaborador atualizados com sucesso'}), 200
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'erro': 'Erro ao atualizar colaborador'}), 400
    
# Endereco/colaborador/deletar/1
@bp_colaborador.route('/deletar/<int:id_colaborador>', methods=['DELETE'])
@swag_from('../docs/colaborador/deletar_colaborador.yml')
def deletar_colaborador(id_colaborador):
    
    colaborador = db.session.query(Colaborador).get(id_colaborador)
    try:
        if not colaborador:
            return jsonify({'erro': 'Colaborador não encontrado'}), 404
            
        db.session.delete(colaborador)
        db.session.commit()

        return jsonify({'mensagem': 'Colaborador deletado com sucesso'}), 200
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({
            'erro': 'Este colaborador possui reembolsos pendentes e não pode ser deletado. '
                    'É necessário tratar os reembolsos antes.'
        }), 400
    
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'erro': 'Erro ao deletar colaborador'}), 400