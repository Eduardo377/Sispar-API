from src.model import db #traz a instancia do SQLALchemy para este arquivo
from sqlalchemy.schema import Column # Traz o recurso para o ORM entender que o atributo será uma coluna na tabela
from sqlalchemy.types import String, DECIMAL, Integer # Importando os tipos de dados que as colunas vão aceitar

class Colaborador(db.Model):
    __tablename__ = "colaborador"
    
#------------------------------ATRIBUTOS-----------------------------
#   id INT AUTO_INCREMENT PRIMARY KEY
    id = Column(Integer, primary_key=True, autoincrement=True)
#   name VARCHAR(100)
    name = Column(String(100))
    email = Column(String(100))
    password = Column(String(255))
    position = Column(String(100))
    wage = Column(DECIMAL(10,2))
#---------------------------------------------------------------------
    def __init__(self, name, email, password, position, wage):
        self.name = name
        self.email = email
        self.password = password
        self.position = position
        self.wage = wage
# ----------------------------------------------------------------------

    def to_dict(self) -> dict:
        return {
            'email': self.email,
            'password': self.password
        }
        
    def all_date(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'position': self.position,
            'wage': self.wage
        }