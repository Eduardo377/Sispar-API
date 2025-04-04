from src.model import db # Instacia do ORM

from sqlalchemy import Column # Vai transformar atributos em colunas

from sqlalchemy.types import String, DECIMAL, Integer # VOu setar Tipos de dados para colunas

class Colaborador(db.Model): # Mapeia e cria entidade no banco de dados
    
#----------------------------------------------------------Atributos----------------------------------------------------------------------------

#   id INT AUTO_INCREMENT PRIMARY KEY,
    id = Column(Integer, primary_key=True, autoincrement=True) # Chave Primaria
    # nome VARCHAR(100)
    nome = Column(String(100)) # Nome do colaborador
    email = Column(String(100)) # Email do colaborador
    senha = Column(String(50)) # Senha do colaborador
    cargo = Column(String(100)) # Cargo do colaborador
    salario = Column(DECIMAL(10, 2)) # Salario do colaborador
#-----------------------------------------------------------------------------------------------------------------------------------------------    
    # Construtor da classe Colaborador
    # Inicializa os atributos com os valores passados como parâmetros
    def __init__(self, nome, email, senha, cargo, salario):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.cargo = cargo
        self.salario = salario