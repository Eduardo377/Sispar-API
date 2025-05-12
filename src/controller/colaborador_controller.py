from flask import Blueprint, request, jsonify
from src.model.colaborador_model import Colaborador
from src.model import db
from src.security.security import hash_password, checar_password
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
    password = dados_requisicao.get('password')
    
    if not email or not password:
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
    
    if email == colaborador.get('email') and checar_password(password, colaborador.get('password')):
        return jsonify({'mensagem': 'Login realizado com sucesso'}), 200
    else:
        return jsonify({'mensagem': 'Credenciais invalidas'}), 400
    
# Endereco/colaborador/cadastrar/1
@bp_colaborador.route('/cadastrar', methods=['POST'])
@swag_from('../docs/colaborador/cadastrar_colaborador.yml')
def cadastrar_novo_colaborador(): 
    
    dados_requisicao = request.get_json()
    
    try:
        password_criptografada = hash_password(dados_requisicao['password'])
        novo_colaborador = Colaborador(
            name=dados_requisicao['name'],
            email=dados_requisicao['email'],
            password=password_criptografada,
            position=dados_requisicao['position'],
            wage=dados_requisicao['wage']
        )
    
#   INSERT INTO tb_colaborador (name, email, password, position, wage) VALUES (VALOR1,VALOR2,VALOR3,VALOR4,VALOR5)
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
        
        if 'name' in dados_requisicao:
            colaborador.name = dados_requisicao['name']
        if 'email' in dados_requisicao:
            colaborador.email = dados_requisicao['email']
        if 'password' in dados_requisicao:
            password_criptografada = hash_password(dados_requisicao['password'])
            colaborador.password = password_criptografada
        if 'position' in dados_requisicao:
            colaborador.position = dados_requisicao['position']
        if 'wage' in dados_requisicao:
            colaborador.wage = dados_requisicao['wage']
            
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