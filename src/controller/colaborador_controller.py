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
    
    if not colaborador:
        return jsonify({'mensagem': 'Usuario não encontrado'}), 404
    
    colaborador = colaborador.to_dict()
    
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
def visualizar_colaborador():
    colaborador = db.session.scalars(
        db.select(Colaborador)
    ).all()
    
    if not colaborador:
        return jsonify({'mensagem': 'Nenhum colaborador encontrado'}), 404
    
    name_colaborador = colaborador
    
    return jsonify([r.all_data() for r in name_colaborador]), 200

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
            'erro': 'Este colaborador possui colaboradors pendentes e não pode ser deletado. '
                    'É necessário tratar os colaboradors antes.'
        }), 400
    
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'erro': 'Erro ao deletar colaborador'}), 400
    
@bp_colaborador.route('/mockar', methods=['POST'])
@swag_from('../docs/colaborador/mockar_colaboradores.yml')
def popular_colaboradores():
    # Lista de colaboradores mockados
    mock_colaboradores = request.get_json()
    if not mock_colaboradores:
        return jsonify({"mensagem": "Nenhum colaborador mockado encontrado!"}), 400

    for item in mock_colaboradores:
        colaborador = Colaborador(
            name=item["name"],
            email=item["email"],
            password=hash_password(item["password"]),
            position=item["position"],
            wage=item["wage"]
        )
        db.session.add(colaborador)
    db.session.commit()
    return jsonify({"mensagem": "✅ Colaboradores cadastrados com sucesso!"}),200