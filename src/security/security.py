from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def hash_senha(senha):
    return bcrypt.generate_password_hash(senha).decode('utf-8')

def checar_senha(senha, senha_hash):
    return bcrypt.check_password_hash(senha_hash, senha)