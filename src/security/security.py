from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

def checar_password(password, password_hash):
    return bcrypt.check_password_hash(password_hash, password)